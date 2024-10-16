from __future__ import annotations
import os
import environ
from pathlib import Path
from core.utils import splitting_var_env


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
if env.str('ENVIRONMENT') == 'dev':
    environ.Env.read_env(os.path.join(BASE_DIR, '.env.dev'))
elif env.str('ENVIRONMENT') == 'prod':
    environ.Env.read_env(os.path.join(BASE_DIR, '.env.prod'))
else:
    raise ValueError('Invalid environment name used in ENVIRONMENT variable in .env file')

ALLOWED_HOSTS = splitting_var_env(env('ALLOWED_HOSTS'))

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'