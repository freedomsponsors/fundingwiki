from functools import wraps
from django.http import JsonResponse, HttpResponseRedirect


def requires_identity(level='guest', api_only=False):
    """
    Decorator para controlar el acceso por nivel de identidad MediaWiki.

    level='guest'       → acepta cualquier cuenta MediaWiki (temporal o registrada)
    level='registered'  → requiere cuenta registrada (is_temp_account=False)
    api_only=True       → devuelve JsonResponse (para API views)
    api_only=False      → redirige a login (para HTML views)

    Uso:
        @requires_identity(level='guest', api_only=True)
        def create_issue(request): ...

        @requires_identity(level='registered', api_only=True)
        def create_offer(request): ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            mw_user = getattr(request, 'mw_user', None)

            if level == 'registered':
                # Requiere cuenta registrada (no temporal)
                if not mw_user or mw_user.is_temp_account:
                    if api_only:
                        return JsonResponse(
                            {'error': 'Esta acción requiere cuenta registrada en MediaWiki'},
                            status=401
                        )
                    else:
                        return HttpResponseRedirect('/login/')
            elif level == 'guest':
                # Acepta cualquier cuenta MediaWiki (temporal o registrada)
                if not mw_user:
                    if api_only:
                        return JsonResponse(
                            {'error': 'Necesitas una cuenta en la wiki para hacer esto'},
                            status=401
                        )
                    else:
                        return HttpResponseRedirect('/login/')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
