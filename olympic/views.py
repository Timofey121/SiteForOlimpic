from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from olympic.forms import RegisterForm, LoginUserForm, SecretTokenForm
from olympic.models import Olympiads, Subjects, SecretToken, NotificationDates, UserNameAndTelegramID
from olympic.utils import menu, additional_menu, DataMixin


def main(request):
    return render(request, 'olympic/main.html',
                  {"menu": menu, "additional_menu": additional_menu, 'title': 'Главная страница'})


def AllOlympiads(request):
    if request.method == "POST":
        if 'someone' in request.POST['select']:
            usr = request.user.username
            if UserNameAndTelegramID.objects.filter(user=request.user.username).exists():
                telegram_id = UserNameAndTelegramID.objects.get(user=request.user.username).telegram_id
                return render(request, 'olympic/list_of_available_subjects.html',
                              {"menu": menu,
                               "additional_menu": additional_menu,
                               'title': 'Олимпиады',
                               'categories': Subjects.objects.all(),
                               'olympiads': NotificationDates.objects.filter(Q(user=telegram_id) | Q(user=usr)).all(),
                               'text': "Показать все олимпиады",
                               'flag': True,
                               })
            return render(request, 'olympic/list_of_available_subjects.html',
                          {"menu": menu,
                           "additional_menu": additional_menu,
                           'title': 'Олимпиады',
                           'categories': Subjects.objects.all(),
                           'olympiads': NotificationDates.objects.filter(user=usr).all(),
                           'text': "Показать все олимпиады",
                           'flag': True,
                           })

    return render(request, 'olympic/list_of_available_subjects.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': 'Олимпиады',
                   'categories': Subjects.objects.all(),
                   'olympiads': Olympiads.objects.all(),
                   'text': "Показать только те олимпиады, к которым у меня подключены уведомления",
                   'flag': False,
                   })


def FilterOlympiads(request, sub_slug):
    c = Subjects.objects.get(slug=sub_slug)
    if request.method == "POST":
        if 'someone' in request.POST['select']:
            usr = request.user.username
            if UserNameAndTelegramID.objects.filter(user=request.user.username).exists():
                telegram_id = UserNameAndTelegramID.objects.get(user=request.user.username).telegram_id
                return render(request, 'olympic/list_of_available_subjects.html',
                              {"menu": menu,
                               "additional_menu": additional_menu,
                               'title': f'Категория - {c.subject}',
                               'categories': Subjects.objects.all(),
                               'olympiads': NotificationDates.objects.filter(
                                   Q(user=telegram_id, sub__slug=sub_slug) | Q(user=usr, sub__slug=sub_slug)).all(),
                               'text': "Показать все олимпиады",
                               "bad_text": f"Нет подключенных уведомлений по предмету {c.subject}!",
                               'flag': True,
                               })
            return render(request, 'olympic/list_of_available_subjects.html',
                          {"menu": menu,
                           "additional_menu": additional_menu,
                           'title': f'Категория - {c.subject}',
                           'categories': Subjects.objects.all(),
                           'olympiads': NotificationDates.objects.filter(user=usr,
                                                                         sub__slug=sub_slug).all(),
                           'text': "Показать все олимпиады",
                           "bad_text": f"Нет подключенных уведомлений по предмету {c.subject}!",
                           'flag': True,
                           })

    return render(request, 'olympic/list_of_available_subjects.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': f'Категория - {c.subject}',
                   'categories': Subjects.objects.all(),
                   'olympiads': Olympiads.objects.filter(sub__slug=sub_slug),
                   'text': "Показать только те олимпиады, к которым у меня подключены уведомления",
                   "bad_text": f"Нет ближайших олимпиад по предмету {c.subject}!",
                   'flag': False,
                   })


def Notification(request):
    if request.method == "POST":

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
                           'categories': Subjects.objects.all(),
                           'text_for_search': search,
                           })

        elif 'cancel' in request.POST:
            return render(request, 'olympic/information_about_subjects.html',
                          {"menu": menu,
                           "additional_menu": additional_menu,
                           'title': 'Подключение/Удаление уведомлений',
                           'olympiads': Olympiads.objects.all(),
                           'categories': Subjects.objects.all(),
                           'text_for_search': '',
                           })

        elif 'add' in request.POST['select']:
            for title in request.POST.getlist('choose'):
                usr = request.user.username
                if not NotificationDates.objects.filter(title=title, user=usr).exists():
                    record = Olympiads.objects.get(title=title)
                    start, stage, schedule, site, sub, rsoch = record.start, record.stage, record.schedule, \
                        record.site, record.sub, record.rsoch
                    NotificationDates.objects.create(user=usr, title=title, start=start, site=site, stage=stage,
                                                     schedule=schedule, sub=sub, rsoch=rsoch)

        elif 'delete' in request.POST['select']:
            for title in request.POST.getlist('choose'):
                usr = request.user.username
                if UserNameAndTelegramID.objects.filter(user=usr).exists():
                    telegram_id = UserNameAndTelegramID.objects.get(user=usr).telegram_id
                    if NotificationDates.objects.filter(title=title, user=telegram_id).exists():
                        NotificationDates.objects.get(title=title).delete()
                if NotificationDates.objects.filter(title=title, user=usr).exists():
                    NotificationDates.objects.get(title=title).delete()

    return render(request, 'olympic/information_about_subjects.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': 'Подключение/Удаление уведомлений',
                   'olympiads': Olympiads.objects.all(),
                   'categories': Subjects.objects.all(),
                   'text_for_search': '',
                   })


def token(request):
    alert_text = ''
    if request.method == 'POST':
        if 'password' in request.POST:
            token = request.POST['password']
            if SecretToken.objects.filter(secret_token=token).exists():
                tg_id = SecretToken.objects.get(secret_token=token).telegram_id
                if not UserNameAndTelegramID.objects.filter(telegram_id=tg_id).exists():
                    UserNameAndTelegramID.objects.create(telegram_id=tg_id, user=request.user)
            else:
                alert_text = 'Нет Телеграмм аккаунта с таким Секретным Токеном'
        else:
            UserNameAndTelegramID.objects.filter(user=request.user).delete()

    usr = request.user.username
    flag = UserNameAndTelegramID.objects.filter(user=usr).exists()
    return render(request, 'olympic/secret_token_pager.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': 'Синхронизация с Телеграмм Ботом',
                   'form': SecretTokenForm(),
                   'flag': flag,
                   'alert_text': alert_text,
                   })


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterForm
    template_name = 'olympic/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'olympic/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)  # выход из авторизации
    return redirect('login')
