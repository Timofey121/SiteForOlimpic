import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SiteForOlimpic.settings')

app = Celery('SiteForOlimpic')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-notification-every-12-hour': {
        'task': 'olympic.tasks.send_notification_email_from_olympic',
        'schedule': crontab(hour='*/12')
    },
    'delete_needs_token_every_day': {
        'task': 'olympic.tasks.delete_token_every_day',
        'schedule': crontab(hour='*/24')
    },
    'add_olympiads_to_bd_every_2.5_day': {
        'task': 'olympic.tasks.add_olympiads',
        'schedule': crontab(minute='*/10')
    },
}
