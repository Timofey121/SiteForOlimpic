from django.core.mail import send_mail
from django.utils.html import strip_tags


def send_email(name_email, user, body):
    send_mail(
        name_email,
        '',
        'from@example.com',
        [user],
        html_message=body,
        fail_silently=False,
    )
