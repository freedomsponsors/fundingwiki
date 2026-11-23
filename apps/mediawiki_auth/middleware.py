"""Resolve the MediaWiki session cookie into the existing Django User model."""
import hashlib
import logging
import re

import requests
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.core.cache import cache
from django.utils.functional import SimpleLazyObject

from .models import MWIdentity

logger = logging.getLogger(__name__)


def _cookie_name():
    return f"{settings.MEDIAWIKI_COOKIE_PREFIX}_session"


def _userinfo(cookie):
    key = "mw-userinfo:" + hashlib.sha256(cookie.encode("utf-8")).hexdigest()
    cached = cache.get(key)
    if cached is not None:
        return cached
    try:
        response = requests.get(
            settings.MEDIAWIKI_INTERNAL_API_URL,
            params={"action": "query", "meta": "userinfo",
                    "uiprop": "groups|rights|blockinfo", "format": "json",
                    "formatversion": 2},
            headers={"Cookie": f"{_cookie_name()}={cookie}",
                     "Host": settings.MEDIAWIKI_API_HOST},
            timeout=settings.MEDIAWIKI_API_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        if "error" in payload:
            logger.warning("MediaWiki userinfo API error: %s", payload["error"])
            return None
        info = payload.get("query", {}).get("userinfo", {})
        cache.set(key, info, settings.MEDIAWIKI_CACHE_TTL)
        return info
    except (requests.RequestException, ValueError, TypeError) as exc:
        logger.warning("MediaWiki userinfo lookup failed: %s", exc)
        return None


def _username(name, mw_id):
    # Django's stock username validator does not allow MediaWiki's '~' temp prefix.
    candidate = name if re.fullmatch(r"[\w.@+-]+", name, flags=re.UNICODE) else f"mw_{mw_id}"
    if User.objects.filter(username=candidate).exclude(mw_identity__mw_id=mw_id).exists():
        candidate = f"mw_{mw_id}"
    if User.objects.filter(username=candidate).exclude(mw_identity__mw_id=mw_id).exists():
        candidate = f"mw_{mw_id}_{hashlib.sha256(name.encode()).hexdigest()[:8]}"
    return candidate[:150]


def _is_valid_username(name):
    return bool(re.fullmatch(r"[\w.@+-]+", name, flags=re.UNICODE))


def _resolve(cookie):
    if not cookie:
        return AnonymousUser()
    info = _userinfo(cookie)
    if not info:
        return AnonymousUser()
    mw_id = info.get("id")
    is_temp = bool(info.get("temp", False))
    if info.get("anon") or not mw_id:
        return AnonymousUser()
    name = info.get("name")
    if not name or not mw_id:
        return AnonymousUser()

    profile = MWIdentity.objects.filter(mw_id=mw_id).select_related("user").first()
    if profile is None:
        # Preserve existing Django content when its username matches the
        # authenticated MediaWiki name; the numeric MW ID becomes authoritative
        # as soon as this one-time link is created.
        user = None
        if _is_valid_username(name):
            user = User.objects.filter(username=name, mw_identity__isnull=True).first()
        if user is None:
            user = User.objects.create_user(username=_username(name, mw_id))
        user.set_unusable_password()
        user.save(update_fields=["password"])
        profile = MWIdentity.objects.create(user=user, mw_id=mw_id, is_temp=is_temp)

    user = profile.user
    new_name = _username(name, mw_id)
    changed = []
    if user.username != new_name:
        user.username = new_name
        changed.append("username")
    if user.has_usable_password():
        user.set_unusable_password()
        changed.append("password")
    admin_group = settings.MEDIAWIKI_ADMIN_GROUP
    is_admin = admin_group in info.get("groups", [])
    if user.is_staff != is_admin:
        user.is_staff = is_admin
        changed.append("is_staff")
    if user.is_superuser != is_admin:
        user.is_superuser = is_admin
        changed.append("is_superuser")
    blocked = bool(info.get("blockedby"))
    profile_changed = []
    if blocked and not profile.is_blocked:
        profile.active_before_block = user.is_active
        profile.is_blocked = True
        profile_changed.extend(["active_before_block", "is_blocked"])
        if user.is_active:
            user.is_active = False
            changed.append("is_active")
    elif profile.is_blocked and not blocked:
        if profile.active_before_block and not user.is_active:
            user.is_active = True
            changed.append("is_active")
        profile.is_blocked = False
        profile.active_before_block = None
        profile_changed.extend(["is_blocked", "active_before_block"])
    if changed:
        user.save(update_fields=changed)
    if profile.is_temp != is_temp:
        profile.is_temp = is_temp
        profile_changed.append("is_temp")
    if profile_changed:
        profile.save(update_fields=profile_changed)
    return user if user.is_active else AnonymousUser()


def _profile_for_request(request):
    user = request.user
    return getattr(user, "mw_identity", None) if user.is_authenticated else None


class MediaWikiIdentityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cookie = request.COOKIES.get(_cookie_name())
        request.user = SimpleLazyObject(lambda: _resolve(cookie))
        # Keep existing identity-aware views working; it resolves lazily too.
        request.mw_user = SimpleLazyObject(lambda: _profile_for_request(request))
        return self.get_response(request)
