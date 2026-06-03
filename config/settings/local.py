from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('DATABASE_NAME', 'djangology'),
        'USER': config('DATABASE_USER', 'djangology'),
        'PASSWORD': config('DATABASE_PASS', 'djangology'),
        'HOST': config('DATABASE_HOST', 'localhost'),
        'PORT': config('DATABASE_PORT', '5432'),
    }
}

REDIS = {
    'host': config('REDIS_HOST', 'localhost'),
    'port': int(config('REDIS_PORT', '6379')),
    'db': 0,
    'pass': '',
}

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8000",
]
