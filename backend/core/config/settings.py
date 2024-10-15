from __future__ import annotations
from split_settings.tools import include

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