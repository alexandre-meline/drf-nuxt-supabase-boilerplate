from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings')

    app = Celery('core')
    app.conf.update(
        broker_connection_retry_on_startup=True,
        broker_connection_max_retries=10,
    )
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks()
    
except Exception as e:
    print(f'Error: {e}')
    raise e
