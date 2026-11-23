from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpResponseRedirect


def mediawiki_login(request):
    next_path = request.GET.get("next", "/")
    if not next_path.startswith("/") or next_path.startswith("//"):
        next_path = "/"
    query = urlencode({"returnto": settings.MEDIAWIKI_SERVER_URL + next_path})
    return HttpResponseRedirect(f"{settings.MEDIAWIKI_SERVER_URL}/doc/Special:UserLogin?{query}")


def mediawiki_logout(request):
    return HttpResponseRedirect(f"{settings.MEDIAWIKI_SERVER_URL}/doc/Special:UserLogout")
