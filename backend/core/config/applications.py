from __future__ import annotations

# Application definition
_INTERNAL_APPS = [
    'user',
]

_THIRD_PARTY_APPS = [
    'rest_framework',
    'django_celery_beat',
    'django_celery_results',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

INSTALLED_APPS.extend(_INTERNAL_APPS)
INSTALLED_APPS.extend(_THIRD_PARTY_APPS)