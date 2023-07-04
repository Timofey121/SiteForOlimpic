import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SiteForOlimpic.settings')

app = Celery('SiteForOlimpic')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# RUN CELERY:
# celery -A SiteForOlimpic worker -l info
# celery -A SiteForOlimpic beat -l info

# RUN FLOWER:
# https://flower.readthedocs.io/en/latest/man.html

# https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
# CREATE TASK, который выполняется каждые 10 минут
app.conf.beat_schedule = {
    'send-notification-every-10-minute': {
        'task': 'olympic.tasks.send_notification_email_from_olympic',
        'schedule': crontab(minute='*/10')
    }
}
