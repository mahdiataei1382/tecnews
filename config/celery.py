from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('django_celery_project')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Tehran')

app.config_from_object(settings, namespace='CELERY')
#celery beat setting
app.conf.beat_schedule = {
    'update_news': {
        'task': 'tecnews.tasks.scraper1',
        'schedule': crontab(hour=23, minute=59),
    }
}
app.autodiscover_tasks()
