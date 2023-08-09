import datetime
import time

import requests
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from selenium import webdriver
from xvfbwrapper import Xvfb

from .models import Subjects, Olympiads, NotificationDates
from .templates.dictionary import numbers, months, months2, subjects_rsosh


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
    subjects = 'Информатика, Математика, Физика, Химия, Биология, География, История, Обществознание, Право, ' \
               'Экономика, Русский язык, Литература, Английский язык, ' \
               'Французский язык, Немецкий язык, Астрономия, Робототехника, ' \
               'Технология, Искусство, Черчение, Психология'.split(', ')

    vdisplay = Xvfb()
    vdisplay.start()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    time.sleep(1)
    for i in range(len(subjects)):
        try:
            sub_id = Subjects.objects.get(subject=subjects[i]).id
            data_start = ''

            URL = f'https://olimpiada.ru/activities?type=any&subject%5B{numbers[subjects[i].strip().capitalize()]}' \
                  f'%5D=on&class=any&period_date=&period=week'
            driver.get(URL)

            while 'Проверка браузера перед переходом на сайт olimpiada.ru' in driver.page_source:
                print('ЖДУ!')
                time.sleep(1)

            for j in range(10):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.05)

            html = driver.page_source

            soup = BeautifulSoup(html, "lxml")

            a = soup.find_all('a', 'none_a black olimp_desc')
            Olympiads.objects.filter(sub=sub_id).all().delete()
            for item in a:
                try:
                    url = "https://olimpiada.ru" + item.get('href')
                    req = requests.get(url=url)
                    src = req.text
                    soup = BeautifulSoup(src, "lxml")
                    title = soup.find_all('title')[0].text.strip().upper()

                    href_olimp = soup.find_all('div', 'contacts')[0].find('a', 'color').get('href')

                    fg = "https://olimpiada.ru" + soup.find_all('tr', 'notgreyclass')[0].find("a").get('href')

                    if fg != 'Расписание олимпиады в этом году пока не известно':
                        url = fg
                        req = requests.get(url=url)
                        src = req.text
                        soup = BeautifulSoup(src, "lxml")

                        step = soup.find('div', 'right').find('h1').text
                        data_start1 = (soup.find('span', 'main_date red').text.strip().replace('\n', '')
                                       .replace('20', ' 20').replace('!', '').replace('До', '')
                                       ).strip().replace(' ', ' ').split('...')[0]

                        for item2 in months2:
                            if item2 in data_start1:
                                data_start1 = data_start1.split(item2.strip())
                                if len(data_start1[0]) == 0:
                                    data_start1 = data_start1[1]

                                data_start = f"{data_start1[-1].strip()}-{months[item2.strip()]}-" \
                                             f"{('0' * (2 - len(data_start1[0].strip())))}{data_start1[0].split('-')[0].strip()}"
                        start = data_start.split('-')
                        try:
                            if len(start[-1]) < 2:
                                start[-1] = '0' + start[-1]
                        except Exception as ex:
                            pass
                        start.reverse()
                        start = '-'.join(start)
                        stage = step
                        schedule = fg
                        site = href_olimp
                        data = datetime.datetime.strptime(''.join(data_start.split("-")), '%Y%m%d').date()
                        now = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y%m%d'), '%Y%m%d').date()
                        if data > now:
                            f = (title in subjects_rsosh[subjects[i].lower().capitalize()])
                            Olympiads.objects.create(title=title, start=start, stage=stage, schedule=schedule,
                                                     site=site, rsoch=f, sub_id=sub_id).save()
                            for tg in NotificationDates.objects.filter(sub_id=sub_id).all():
                                if NotificationDates.objects.filter(tg.user, title, start, stage, schedule, site, f,
                                                                    sub_id).exists():
                                    flag = bool(NotificationDates.objects.get(tg.user, sub_id).rsoch)
                                    if (flag is False) or (f is True and flag is True):
                                        NotificationDates.objects.create(tg.user, title, start, stage, schedule, site,
                                                                         f, sub_id).save()
                except Exception as ex:
                    pass
        except Exception as ex:
            pass

    driver.close()
    vdisplay.stop()
