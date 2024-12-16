from .base import *
import logging

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INSTALLED_APPS += ['nplusone.ext.django', 'debug_toolbar']

MIDDLEWARE += ['nplusone.ext.django.NPlusOneMiddleware', 'debug_toolbar.middleware.DebugToolbarMiddleware']

INTERNAL_IPS = [
    "127.0.0.1",
]

NPLUSONE_LOGGER = logging.getLogger('nplusone')
NPLUSONE_LOG_LEVEL = logging.WARN

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'nplusone': {
            'handlers': ['console'],
            'level': 'WARN',
        },
    },
}
