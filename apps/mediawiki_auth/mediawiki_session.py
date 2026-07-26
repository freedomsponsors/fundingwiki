import requests
from django.conf import settings

MW_API = settings.MEDIAWIKI_URL + '/doc/api.php'

def verify_mediawiki_session(mw_session_cookie: str) -> dict | None:
    """
    Verifica una cookie de sesión MediaWiki.
    Devuelve info del usuario si es válida (incluyendo cuentas temporales),
    None si la sesión no existe o expiró.
    """
    try:
        resp = requests.get(
            MW_API,
            params={
                'action':  'query',
                'meta':    'userinfo',
                'uiprop':  'groups|rights',
                'format':  'json',
            },
            cookies={'mediawiki_session': mw_session_cookie},
            timeout=3,
        )
        resp.raise_for_status()
        data = resp.json()
        userinfo = data.get('query', {}).get('userinfo', {})

        # ID 0 = anónimo puro sin cookie válida
        if userinfo.get('id', 0) == 0 and not userinfo.get('temp'):
            return None

        return {
            'mw_id':   userinfo.get('id'),          # 0 para cuentas temporales
            'name':    userinfo.get('name'),         # "~2026-4521983" o "Pepito"
            'is_temp': userinfo.get('temp', False),  # True para cuentas temporales
            'groups':  userinfo.get('groups', []),
        }
    except requests.RequestException:
        return None
