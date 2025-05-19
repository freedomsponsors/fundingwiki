from decouple import config

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
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'pass': '',
}
