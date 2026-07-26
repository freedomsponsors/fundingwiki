from .mediawiki_session import verify_mediawiki_session
from .models import MWUser


class MediaWikiIdentityMiddleware:
    """
    Enriquece el request con la identidad MediaWiki del usuario.
    Usa solo MWUser para todos los usuarios (temporales y registrados).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Intentar identificar por cookie de sesión MediaWiki
        mw_cookie = request.COOKIES.get('mediawiki_session')
        if mw_cookie:
            mw_info = verify_mediawiki_session(mw_cookie)
            if mw_info:
                guest, _ = MWUser.objects.get_or_create(
                    mw_session_cookie=mw_cookie,
                    defaults={
                        'mw_temp_name': mw_info['name'],
                        'is_temp_account': mw_info['is_temp'],
                    }
                )
                # Actualizar is_temp_account si cambió (ej: usuario temporal se registró)
                if guest.is_temp_account != mw_info['is_temp']:
                    guest.is_temp_account = mw_info['is_temp']
                    guest.mw_temp_name = mw_info['name']
                    guest.save()

                request.mw_user = guest
                request.mw_identity = mw_info
            else:
                request.mw_user = None
                request.mw_identity = None
        else:
            request.mw_user = None
            request.mw_identity = None

        return self.get_response(request)
