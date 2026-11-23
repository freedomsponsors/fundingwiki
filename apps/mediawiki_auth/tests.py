from unittest.mock import Mock, patch

import requests
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.core.cache import cache
from django.test import RequestFactory, TestCase, override_settings

from .middleware import MediaWikiIdentityMiddleware
from .middleware import _cookie_name
from .models import MWIdentity


@override_settings(MEDIAWIKI_COOKIE_PREFIX="testwiki", MEDIAWIKI_CACHE_TTL=20,
                   MEDIAWIKI_INTERNAL_API_URL="http://mediawiki/api.php",
                   MEDIAWIKI_API_HOST="wiki.test", MEDIAWIKI_API_TIMEOUT=1,
                   MEDIAWIKI_ADMIN_GROUP="sysop")
class MediaWikiIdentityMiddlewareTests(TestCase):
    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()

    def resolve(self, cookie=None):
        headers = {"HTTP_COOKIE": f"{_cookie_name()}={cookie}"} if cookie else {}
        request = self.factory.get("/", **headers)
        if cookie:
            self.assertEqual(request.COOKIES.get(_cookie_name()), cookie)

        def resolve_user(req):
            user = req.user
            # Resolve inside the mock context; the production middleware stays lazy.
            user.is_authenticated
            return user

        middleware = MediaWikiIdentityMiddleware(resolve_user)
        return middleware(request)

    def test_cookie_name_uses_configured_prefix(self):
        self.assertEqual(settings.MEDIAWIKI_COOKIE_PREFIX, "testwiki")
        self.assertEqual(_cookie_name(), "testwiki_session")

    @staticmethod
    def api_response(info):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"query": {"userinfo": info}}
        return response

    def test_no_cookie_is_anonymous_without_api_call(self):
        with patch("apps.mediawiki_auth.middleware.requests.get") as get:
            self.assertIsInstance(self.resolve(), AnonymousUser)
            get.assert_not_called()

    def test_registered_user_is_created_with_unusable_password_and_renamed(self):
        with patch("apps.mediawiki_auth.middleware._userinfo", return_value=
                   {"id": 42, "name": "Ada", "groups": ["user"]}):
            user = self.resolve("registered")
        self.assertEqual(user.username, "Ada")
        self.assertFalse(user.has_usable_password())
        self.assertEqual(user.mw_identity.mw_id, 42)
        cache.clear()
        with patch("apps.mediawiki_auth.middleware._userinfo", return_value=
                   {"id": 42, "name": "AdaRenamed", "groups": ["user"]}):
            user = self.resolve("registered")
        self.assertEqual(user.username, "AdaRenamed")

    def test_temporary_user_is_mapped_and_marked(self):
        with patch("apps.mediawiki_auth.middleware._userinfo", return_value=
                   {"id": 77, "name": "~2026-77", "temp": True, "groups": ["user"]}):
            user = self.resolve("temporary")
        self.assertTrue(user.mw_identity.is_temp)
        self.assertFalse(user.has_usable_password())

    def test_existing_django_account_is_linked_without_losing_its_id(self):
        existing = User.objects.create_user(username="Legacy", password="old-password")
        with patch("apps.mediawiki_auth.middleware._userinfo", return_value=
                   {"id": 78, "name": "Legacy", "groups": ["user"]}):
            user = self.resolve("legacy")
        self.assertEqual(user.pk, existing.pk)
        self.assertFalse(user.has_usable_password())
        self.assertEqual(user.mw_identity.mw_id, 78)

    def test_anonymous_flag_is_anonymous(self):
        with patch("apps.mediawiki_auth.middleware._userinfo", return_value=
                   {"id": 0, "anon": True}):
            self.assertIsInstance(self.resolve("anonymous-cookie"), AnonymousUser)

    def test_sysop_grants_and_losing_group_removes_admin_flags(self):
        with patch("apps.mediawiki_auth.middleware._userinfo", return_value=
                   {"id": 12, "name": "Admin", "groups": ["sysop"]}):
            user = self.resolve("admin")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        cache.clear()
        with patch("apps.mediawiki_auth.middleware._userinfo", return_value=
                   {"id": 12, "name": "Admin", "groups": ["user"]}):
            user = self.resolve("admin")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_block_then_unblock_controls_active_state(self):
        with patch("apps.mediawiki_auth.middleware._userinfo", return_value=
                   {"id": 13, "name": "Blocked", "groups": ["user"], "blockedby": "Sysop"}):
            self.assertIsInstance(self.resolve("blocked"), AnonymousUser)
        user = User.objects.get(username="Blocked")
        self.assertFalse(user.is_active)
        cache.clear()
        with patch("apps.mediawiki_auth.middleware._userinfo", return_value=
                   {"id": 13, "name": "Blocked", "groups": ["user"]}):
            user = self.resolve("blocked")
        self.assertTrue(user.is_active)
        self.assertFalse(user.mw_identity.is_blocked)

    def test_api_failure_fails_closed_as_anonymous(self):
        with patch("apps.mediawiki_auth.middleware.requests.get", side_effect=requests.Timeout("offline")):
            self.assertIsInstance(self.resolve("offline"), AnonymousUser)

    def test_same_cookie_uses_cache(self):
        with patch("apps.mediawiki_auth.middleware.requests.get", return_value=self.api_response(
                {"id": 19, "name": "Cached", "groups": ["user"]})) as get:
            first = self.resolve("cached")
            second = self.resolve("cached")
        self.assertEqual(first.pk, second.pk)
        get.assert_called_once()
        self.assertEqual(MWIdentity.objects.count(), 1)
