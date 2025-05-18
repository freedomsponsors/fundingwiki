from .base import *
from decouple import config

current_env = config('DJANGO_ENV', 'local')

if current_env == 'production':
    from .production import *
elif current_env == 'development':
    from .development import *
else:
    from .local import *