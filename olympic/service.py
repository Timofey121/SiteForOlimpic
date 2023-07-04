from django.core.mail import send_mail
from django.utils.html import strip_tags


def send_email(user, body):
    send_mail(
        'Сброс-Пароля-[olympic]',
        strip_tags(body),
        'from@example.com',
        [user],
        fail_silently=False,
    )
