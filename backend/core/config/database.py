from __future__ import annotations
from .base import env

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if env.bool('USE_SQLITE'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': "db.sqlite3",
        }
    }
else:
    DATABASES = {
        'default': env.db()
    }