from django.core.mail import send_mail


def send_email(name_email, user, body):
    send_mail(
        name_email,
        '',
        'from@example.com',
        [user],
        html_message=body,
        fail_silently=False,
    )


def translate_english_letters_into_russian(text: str):
    layout = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                               'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                      "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                      'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))
    return text.translate(layout)


def add_olympiads_to_bd():
    pass
