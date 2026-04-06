from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Afficher les emails dans la console en dev
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# DRF — ajouter BrowsableAPI en dev
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

# Logging détaillé en dev
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}

INSTALLED_APPS += ['django_extensions']
