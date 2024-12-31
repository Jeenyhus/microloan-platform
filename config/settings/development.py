from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email Configuration for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS Configuration for development
CORS_ALLOW_ALL_ORIGINS = True 