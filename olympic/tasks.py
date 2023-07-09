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
            if len(final_notifications) > 0:
                html_body = render_to_string('olympic/email_templates/email_notification.html', {
                    'notification': final_notifications,
                })
                send_email('Подключенные уведомления', user.email, html_body)


@app.task
def delete_token_every_day():
    all_token = ResetPassword.objects.all()
    for itm in all_token:
        data_created = itm.data_created
        now = datetime.datetime.now().date()
        flag = ((now - data_created) >= datetime.timedelta(days=1))
        if flag is True:
            ResetPassword.objects.filter(data_created=data_created).delete()
