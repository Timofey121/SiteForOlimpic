from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from olympic.forms import LoginUserForm
from olympic.models import Olympiads, Subjects, SecretToken, NotificationDates
from olympic.utils import menu, DataMixin, additional_menu


def main(request):
    return render(request, 'olympic/main.html',
                  {"menu": menu, "additional_menu": additional_menu, 'title': 'Главная страница'})


def AllOlympiads(request):
    if request.method == "POST":
        if 'someone' in request.POST['select']:
            if SecretToken.objects.filter(secret_token=request.user.username).exists():
                telegram_id = SecretToken.objects.filter(secret_token=request.user.username)[0]
                return render(request, 'olympic/list_of_available_subjects.html',
                              {"menu": menu,
                               "additional_menu": additional_menu,
                               'title': 'Олимпиады',
                               'categories': Subjects.objects.all(),
                               'olympiads': NotificationDates.objects.filter(user=telegram_id).all(),
                               'text': "Показать все олимпиады"})
            else:
                usr = request.user.username
                return render(request, 'olympic/list_of_available_subjects.html',
                              {"menu": menu,
                               "additional_menu": additional_menu,
                               'title': 'Олимпиады',
                               'categories': Subjects.objects.all(),
                               'olympiads': NotificationDates.objects.filter(user=usr).all(),
                               'text': "Показать все олимпиады"})

    return render(request, 'olympic/list_of_available_subjects.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': 'Олимпиады',
                   'categories': Subjects.objects.all(),
                   'olympiads': Olympiads.objects.all(),
                   'text': "Показать только те олимпиады, к которым у меня подключены уведомления"})


def FilterOlympiads(request, sub_slug):
    c = Subjects.objects.get(slug=sub_slug)
    if request.method == "POST":
        if 'someone' in request.POST['select']:
            if SecretToken.objects.filter(secret_token=request.user.username).exists():
                telegram_id = SecretToken.objects.filter(secret_token=request.user.username)[0]
                return render(request, 'olympic/list_of_available_subjects.html',
                              {"menu": menu,
                               "additional_menu": additional_menu,
                               'title': f'Категория - {c.subject}',
                               'categories': Subjects.objects.all(),
                               'olympiads': NotificationDates.objects.filter(user=telegram_id,
                                                                             sub__slug=sub_slug).all(),
                               'text': "Показать все олимпиады",
                               "bad_text": f"Нет подключенных уведомлений по предмету {c.subject}!",
                               'c': c
                               })
            else:
                usr = request.user.username
                return render(request, 'olympic/list_of_available_subjects.html',
                              {"menu": menu,
                               "additional_menu": additional_menu,
                               'title': f'Категория - {c.subject}',
                               'categories': Subjects.objects.all(),
                               'olympiads': NotificationDates.objects.filter(user=usr,
                                                                             sub__slug=sub_slug).all(),
                               'text': "Показать все олимпиады",
                               "bad_text": f"Нет подключенных уведомлений по предмету {c.subject}!",
                               'c': c
                               })

    return render(request, 'olympic/list_of_available_subjects.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': f'Категория - {c.subject}',
                   'categories': Subjects.objects.all(),
                   'olympiads': Olympiads.objects.filter(sub__slug=sub_slug),
                   'text': "Показать только те олимпиады, к которым у меня подключены уведомления",
                   "bad_text": f"Нет ближайших олимпиад по предмету {c.subject}!",
                   'c': c
                   })


def Notification(request):
    if request.method == "POST":
        print(request.POST)

        if 'find' in request.POST:
            search = str(request.POST['search'])
            search_olympiads = list(Olympiads.objects.filter(
                Q(title__contains=search) | Q(title__contains=search.capitalize()) | Q(
                    title__contains=search.lower())))
            for itm in Subjects.objects.filter(
                    Q(subject__contains=search.capitalize()) | Q(subject__contains=search) | Q(
                        subject__contains=search.lower())).values():
                sub_slug = itm['slug']
                search_olympiads += list(Olympiads.objects.filter(Q(sub__slug__contains=sub_slug)))
            return render(request, 'olympic/information_about_subjects.html',
                          {"menu": menu,
                           "additional_menu": additional_menu,
                           'title': 'Подключение/Удаление уведомлений',
                           'olympiads': search_olympiads,
                           'message': f"Ваш запрос в поиске → {search}",
                           'categories': Subjects.objects.all(),
                           'text_for_search': search,
                           })

        elif 'cancel' in request.POST:
            return render(request, 'olympic/information_about_subjects.html',
                          {"menu": menu,
                           "additional_menu": additional_menu,
                           'title': 'Подключение/Удаление уведомлений',
                           'olympiads': Olympiads.objects.all(),
                           'message': '',
                           'categories': Subjects.objects.all(),
                           'text_for_search': '',
                           })

        # elif 'choice' in request.POST:
        #     if request.POST['select-action'] == 'connect':
        #         for key, val in request.POST.items():
        #             if ('yes_no' in key) and val == 'on':
        #                 title = str(key).replace('yes_no_', '')
        #                 telegram_id = SecretToken.objects.filter(secret_token=request.user.username)[0]
        #                 if not NotificationDates.objects.filter(title=title, telegram_id=telegram_id).exists():
        #                     record = Olympiads.objects.get(title=title)
        #                     start, stage, schedule, site, sub, rsoch = record.start, record.stage, record.schedule, \
        #                         record.site, record.sub, record.rsoch
        #                     NotificationDates.objects.create(telegram_id=telegram_id, title=title, start=start,
        #                                                      site=site, stage=stage, schedule=schedule,
        #                                                      sub=sub, rsoch=rsoch)
        #     elif request.POST['select-action'] == 'delete':
        #         for key, val in request.POST.items():
        #             if ('yes_no' in key) and val == 'on':
        #                 title = str(key).replace('yes_no_', '')
        #                 telegram_id = SecretToken.objects.filter(secret_token=request.user.username)[0]
        #                 if NotificationDates.objects.filter(title=title, telegram_id=telegram_id).exists():
        #                     NotificationDates.objects.get(title=title).delete()

    return render(request, 'olympic/information_about_subjects.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': 'Подключение/Удаление уведомлений',
                   'olympiads': Olympiads.objects.all(),
                   'message': '',
                   'categories': Subjects.objects.all(),
                   'text_for_search': '',
                   })


def RegisterUser(request):
    return render(request, 'olympic/login1.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': 'Регистрация',
                   })


def LoginUser(request):
    pass


def logout_user(request):
    logout(request)  # выход из авторизации
    return redirect('login')
