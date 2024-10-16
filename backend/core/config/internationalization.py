from __future__ import annotations
from .base import env

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = env.str('LANGUAGE_CODE', default='en-us')

TIME_ZONE = env.str('TIME_ZONE', default='UTC')

USE_I18N = True

USE_TZ = True