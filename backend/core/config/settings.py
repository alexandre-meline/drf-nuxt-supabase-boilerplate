from __future__ import annotations
from split_settings.tools import include
from .base import env

if env.str('ENVIRONMENT') == 'dev':
    print('Environment is dev')
    include(
        'applications.py',
        'base.py',
        'database.py',
        'cache.py',
        'celery.py',
        'documentation.py',
        'frontend.py',
        'internationalization.py',
        'logging.py',
        'middleware.py',
        'rest.py',
        'security.py',
        'supabase.py',
    )
elif env.str('ENVIRONMENT') == 'prod':
    print('Environment is prod')
    include(
        'applications.py',
        'base.py',
        'database.py',
        'cache.py',
        'celery.py',
        'documentation.py',
        'frontend.py',
        'internationalization.py',
        'logging.py',
        'middleware.py',
        'rest.py',
        'security.py',
        'supabase.py',
        'sentry.py',
    )
else:
    raise ValueError('Invalid environment name used in ENVIRONMENT variable in .env file')