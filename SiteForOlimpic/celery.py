import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SiteForOlimpic.settings')

app = Celery('SiteForOlimpic')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-notification': {
        'task': 'olympic.tasks.send_notification_email',
        'schedule': crontab(hour='*/12')
    },
    'delete_token': {
        'task': 'olympic.tasks.delete_token_in_bd',
        'schedule': crontab(hour='*/24')
    },
    'add_olympiads': {
        'task': 'olympic.tasks.add_olympiads',
        'schedule': crontab(hour='*/60')
    },
}
