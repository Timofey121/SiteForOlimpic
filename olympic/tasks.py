import datetime

from django.template.loader import render_to_string

from SiteForOlimpic.celery import app
from .models import RegistrationSite, UserNameAndTelegramID, NotificationDates, Olympiads, ResetPassword
from .service import send_email


@app.task
def send_span_email(name_email, user_email, body):
    send_email(name_email, user_email, body)


@app.task
def send_notification_email_from_olympic():
    all_users = RegistrationSite.objects.all()
    for user in all_users:
        if not UserNameAndTelegramID.objects.filter(user=user).exists():
            notifications = NotificationDates.objects.filter(user=user.user).all()
            final_notifications = []
            for notif in notifications:
                data = datetime.datetime.strptime(''.join(str(notif.start).split("-")), '%d%m%Y').date()
                now = datetime.datetime.strptime(datetime.datetime.today().strftime('%d%m%Y'), '%d%m%Y').date()
                if data < now:
                    notifications.filter(title=notif.title, start=notif.start, sub=notif.sub).all().delete()
                    Olympiads.objects.filter(title=notif.title, start=notif.start, sub=notif.sub).all().delete()
                flag = ((data - now) <= datetime.timedelta(days=2))
                flag1 = ((data - now) > datetime.timedelta(days=0))
                if flag is True and flag1 is True:
                    final_notifications.append(notif)
            html_body = render_to_string('olympic/email_templates/email_notification.html', {
                'notification': final_notifications,
            })
            send_email('Подключенные уведомления', user.email, html_body)


@app.task
def delete_token_every_24_hours():
    all_token = ResetPassword.objects.all()
    for itm in all_token:
        data_created = datetime.datetime.strptime(itm.data_created, '%H:%M %d.%m.%Y').date()
        now = datetime.datetime.strptime(datetime.datetime.today().strftime('%H:%M %d.%m.%Y'), '%H:%M %d.%m.%Y').date()
        flag = ((data_created - now) > datetime.timedelta(hours=24))
        flag1 = ((data_created - now) < datetime.timedelta(hours=0))
        if flag is True or flag1 is True:
            ResetPassword.objects.filter(user=itm.user, token=itm.token, data_created=data_created).delete()
