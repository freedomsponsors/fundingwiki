from django.conf import settings
from django.http import HttpResponseRedirect


def mediawiki_login(request):
    # MediaWiki's `returnto` parameter is a wiki page title, not a URL. Passing
    # Django's `next` URL here makes MediaWiki interpret it as a page title
    # (for example, /doc/Https://funding.wiki/admin/). The user can revisit the
    # requested Django page after authenticating at MediaWiki.
    return HttpResponseRedirect(
        f"{settings.MEDIAWIKI_SERVER_URL}/doc/Special:UserLogin"
    )


def mediawiki_logout(request):
    return HttpResponseRedirect(f"{settings.MEDIAWIKI_SERVER_URL}/doc/Special:UserLogout")
