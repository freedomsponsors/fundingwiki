import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.mediawiki_auth.models import MWIdentity


class Command(BaseCommand):
    help = "Deactivate Django users whose MediaWiki temporary accounts expired."

    def handle(self, *args, **options):
        continuation = {}
        deactivated = 0
        while True:
            params = {"action": "query", "list": "allusers",
                      "auprop": "tempexpired", "aulimit": "max",
                      "format": "json", "formatversion": 2, **continuation}
            try:
                response = requests.get(settings.MEDIAWIKI_INTERNAL_API_URL,
                                        params=params, headers={"Host": settings.MEDIAWIKI_API_HOST},
                                        timeout=settings.MEDIAWIKI_API_TIMEOUT)
                response.raise_for_status()
                data = response.json()
            except (requests.RequestException, ValueError) as exc:
                raise CommandError(f"MediaWiki allusers API failed: {exc}") from exc
            if "error" in data:
                raise CommandError(f"MediaWiki API error: {data['error']}")
            for entry in data.get("query", {}).get("allusers", []):
                if entry.get("tempexpired"):
                    user_id = entry.get("userid")
                    profile = MWIdentity.objects.select_related("user").filter(mw_id=user_id, is_temp=True).first()
                    if profile and profile.user.is_active:
                        profile.user.is_active = False
                        profile.user.save(update_fields=["is_active"])
                        deactivated += 1
            continuation = data.get("continue")
            if not continuation:
                break
        self.stdout.write(self.style.SUCCESS(f"Deactivated {deactivated} expired temporary account(s)."))
