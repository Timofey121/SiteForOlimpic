from SiteForOlimpic.celery import app
from .service import send_email


# https://www.youtube.com/playlist?list=PLF-NY6ldwAWqjBkanP1Tl50kDpIYXJBna

@app.task
def send_span_email(user_email, body):
    send_email(user_email, body)


@app.task
def send_notification_email_from_olympic():
    pass
