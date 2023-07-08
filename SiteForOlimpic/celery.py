import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SiteForOlimpic.settings')

app = Celery('SiteForOlimpic', broker='redis://redis:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# CREATE TASK, который выполняется каждые 12 часов
app.conf.beat_schedule = {
    'send-notification-every-12-hour': {
        'task': 'olympic.tasks.send_notification_email_from_olympic',
        'schedule': crontab(hour='*/12')
    },
    'delete_needs_token_every_24_hours': {
        'task': 'olympic.tasks.delete_token_every_24_hours',
        'schedule': crontab(hour='*/24')
    },
}
