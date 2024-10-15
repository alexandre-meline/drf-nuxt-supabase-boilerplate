from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import os

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings')

    app = Celery('core')
    app.conf.update(
        broker_connection_retry_on_startup=True,
    )
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks()
    
except Exception as e:
    print(f'Error: {e}')
    raise e
