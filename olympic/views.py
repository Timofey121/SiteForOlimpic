import datetime
from secrets import token_hex

from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm, LoginUserForm, SecretTokenForm, PasswordReset, PasswordResetForUser
from .models import Olympiads, Subjects, SecretToken, NotificationDates, UserNameAndTelegramID, RegistrationSite, \
    ResetPassword
from .service import translate_english_letters_into_russian
from .tasks import send_span_email
from .utils import menu, additional_menu, DataMixin


def pagination(search_olympiads, request):
    all_olympiads = search_olympiads
    paginator = Paginator(all_olympiads, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj, paginator


def main(request):
    return render(request, 'olympic/main.html',
                  {"menu": menu, "additional_menu": additional_menu, 'title': 'Главная страница'})


def AllOlympiads(request):
    if request.method == "POST":
        if 'someone' in request.POST['select']:
            usr = request.user
            if UserNameAndTelegramID.objects.filter(customer=request.user.username).exists():
                telegram_id = UserNameAndTelegramID.objects.get(customer=request.user.username).telegram_id
                g = NotificationDates.objects.filter(customer=telegram_id).all()
                h = NotificationDates.objects.filter(customer=usr).all()
                gen = []
                for itm in h:
                    if not g.filter(title=itm.title, start=itm.start, sub_id=itm.sub).exists():
                        gen.append(itm)
                page_obj, paginator = pagination(gen + list(g), request)
                return render(request, 'olympic/list_of_available_subjects.html',
                              {"menu": menu,
                               "additional_menu": additional_menu,
                               'title': 'Олимпиады',
                               'categories': Subjects.objects.all(),
                               'olympiads': gen + list(g),
                               'text': "Показать все олимпиады",
                               'page_obj': page_obj,
                               'paginator': paginator,
                               'flag': True,
                               })

            page_obj, paginator = pagination(NotificationDates.objects.filter(customer=usr).all(), request)
            return render(request, 'olympic/list_of_available_subjects.html',
                          {"menu": menu,
                           "additional_menu": additional_menu,
                           'title': 'Олимпиады',
                           'categories': Subjects.objects.all(),
                           'text': "Показать все олимпиады",
                           'page_obj': page_obj,
                           'paginator': paginator,
                           'flag': True,
                           })

    page_obj, paginator = pagination(Olympiads.objects.all(), request)
    return render(request, 'olympic/list_of_available_subjects.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': 'Олимпиады',
                   'categories': Subjects.objects.all(),
                   'page_obj': page_obj,
                   'paginator': paginator,
                   'text': "Показать только те олимпиады, к которым у меня подключены уведомления",
                   'flag': False,
                   })


def FilterOlympiads(request, sub_slug):
    c = Subjects.objects.get(slug=sub_slug)
    if request.method == "POST":
        if 'someone' in request.POST['select']:
            usr = request.user.username
            if UserNameAndTelegramID.objects.filter(customer=request.user.username).exists():
                telegram_id = UserNameAndTelegramID.objects.get(customer=request.user.username).telegram_id
                g = NotificationDates.objects.filter(customer=telegram_id, sub__slug=sub_slug).all()
                h = NotificationDates.objects.filter(customer=usr, sub__slug=sub_slug).all()
                gen = []
                for itm in h:
                    if not g.filter(title=itm.title, start=itm.start, sub_id=itm.sub).exists():
                        gen.append(itm)

                page_obj, paginator = pagination(gen + list(g), request)
                return render(request, 'olympic/list_of_available_subjects.html',
                              {"menu": menu,
                               "additional_menu": additional_menu,
                               'title': f'Категория - {c.subject}',
                               'categories': Subjects.objects.all(),
                               'text': "Показать все олимпиады",
                               'page_obj': page_obj,
                               'paginator': paginator,
                               "bad_text": f"Нет подключенных уведомлений по предмету {c.subject}!",
                               'flag': True,
                               })

            page_obj, paginator = pagination(NotificationDates.objects.filter(customer=usr, sub__slug=sub_slug).all(), request)
            return render(request, 'olympic/list_of_available_subjects.html',
                          {"menu": menu,
                           "additional_menu": additional_menu,
                           'title': f'Категория - {c.subject}',
                           'categories': Subjects.objects.all(),
                           'text': "Показать все олимпиады",
                           "bad_text": f"Нет подключенных уведомлений по предмету {c.subject}!",
                           'flag': True,
                           'paginator': paginator,
                           'page_obj': page_obj,
                           })
    page_obj, paginator = pagination(Olympiads.objects.filter(sub__slug=sub_slug), request)
    return render(request, 'olympic/list_of_available_subjects.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': f'Категория - {c.subject}',
                   'categories': Subjects.objects.all(),
                   'text': "Показать только те олимпиады, к которым у меня подключены уведомления",
                   'page_obj': page_obj,
                   'paginator': paginator,
                   "bad_text": f"Нет ближайших олимпиад по предмету {c.subject}!",
                   'flag': False,
                   })


def Notification(request):
    if not request.user.is_authenticated:
        return redirect('home')
    page_obj, paginator = pagination(Olympiads.objects.all(), request)
    if request.method == "POST":
        if 'find' in request.POST:
            search = str(request.POST['search'])
            translate_search = translate_english_letters_into_russian(search)
            search_olympiads = list(
                Olympiads.objects.filter(
                    Q(title__contains=search) |
                    Q(title__contains=search.capitalize()) |
                    Q(title__contains=search.lower()) |
                    Q(title__contains=translate_search) |
                    Q(title__contains=translate_search.capitalize()) |
                    Q(title__contains=translate_search.lower())
                )
            )
            for itm in Subjects.objects.filter(
                    Q(subject__contains=search.capitalize()) |
                    Q(subject__contains=search) |
                    Q(subject__contains=search.lower()) |
                    Q(subject__contains=translate_search.capitalize()) |
                    Q(subject__contains=translate_search) |
                    Q(subject__contains=translate_search.lower())
            ).values():
                sub_slug = itm['slug']
                search_olympiads += list(Olympiads.objects.filter(Q(sub__slug__contains=sub_slug)))

            page_obj, paginator = pagination(search_olympiads, request)
            return render(request, 'olympic/information_about_subjects.html',
                          {"menu": menu,
                           "additional_menu": additional_menu,
                           'title': 'Подключение/Удаление уведомлений',
                           'page_obj': page_obj,
                           'paginator': paginator,
                           'categories': Subjects.objects.all(),
                           'text_for_search': search,
                           })

        elif 'cancel' in request.POST:
            return render(request, 'olympic/information_about_subjects.html',
                          {"menu": menu,
                           "additional_menu": additional_menu,
                           'title': 'Подключение/Удаление уведомлений',
                           'page_obj': page_obj,
                           'paginator': paginator,
                           'categories': Subjects.objects.all(),
                           'text_for_search': '',
                           })

        elif 'add' in request.POST['select']:
            for itm in request.POST.getlist('choose'):
                title, sub = itm.split('это_!!!_бу-бу_разделитель')
                sub_id = Subjects.objects.get(subject=sub).id
                usr = request.user.username
                if not NotificationDates.objects.filter(title=title, customer=usr, sub=sub_id).exists():
                    record = Olympiads.objects.get(title=title, sub_id=sub_id)
                    start, stage, schedule, site, sub, rsoch = record.start, record.stage, record.schedule, \
                        record.site, record.sub, record.rsoch
                    NotificationDates.objects.create(customer=usr, title=title, start=start, site=site, stage=stage,
                                                     schedule=schedule, sub=sub, rsoch=rsoch)

        elif 'delete' in request.POST['select']:
            for itm in request.POST.getlist('choose'):
                title, sub_name = itm.split('это_!!!_бу-бу_разделитель')
                sub = Subjects.objects.get(subject=sub_name).id
                usr = request.user.username
                if UserNameAndTelegramID.objects.filter(customer=usr).exists():
                    telegram_id = UserNameAndTelegramID.objects.get(customer=usr).telegram_id
                    if NotificationDates.objects.filter(title=title, customer=telegram_id, sub=sub).exists():
                        NotificationDates.objects.get(title=title, customer=telegram_id, sub=sub).delete()
                if NotificationDates.objects.filter(title=title, customer=usr, sub=sub).exists():
                    NotificationDates.objects.get(title=title, customer=usr, sub=sub).delete()

    return render(request, 'olympic/information_about_subjects.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': 'Подключение/Удаление уведомлений',
                   'page_obj': page_obj,
                   'paginator': paginator,
                   'categories': Subjects.objects.all(),
                   'text_for_search': '',
                   })


def password_reset(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        usr_or_email, usr = request.POST['login_or_email'], ''
        if RegistrationSite.objects.filter(customer=usr_or_email).exists():
            usr = RegistrationSite.objects.get(customer=usr_or_email)
        elif RegistrationSite.objects.filter(email=usr_or_email).exists():
            usr = RegistrationSite.objects.get(email=usr_or_email)
        if usr != '':
            tkn = token_hex(32)
            reset_url = (request.build_absolute_uri() + tkn)
            data = {
                'username': usr.customer,
                'url': reset_url,
            }
            html_body = render_to_string('olympic/email_templates/reset_password.html', data)
            now = datetime.datetime.now().strftime('%Y-%m-%d')
            ResetPassword.objects.create(customer=usr.customer, token=tkn, data_created=now)
            send_span_email.delay('Сброс-Пароля-[olympic]', usr.email, html_body)
            return redirect('login')
    return render(request, 'olympic/password_reset.html', {
        "menu": menu,
        "additional_menu": additional_menu,
        'title': 'Сброс Пароля',
        'form': PasswordReset(),
    })


def password_reset_for_usr(request, token):
    if not ResetPassword.objects.filter(token=token).exists():
        return redirect('home')
    if request.method == 'POST':
        new_password = request.POST['new_password']
        username = ResetPassword.objects.get(token=token).customer
        u = User.objects.get(username__exact=username)
        u.set_password(new_password)
        u.save()
        ResetPassword.objects.get(token=token).delete()
        return redirect('login')
    return render(request, 'olympic/password_reset_for_usr.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': 'Сброс Пароля',
                   'form': PasswordResetForUser(),
                   })


def token(request):
    if not request.user.is_authenticated:
        return redirect('home')
    alert_text = ''
    if request.method == 'POST':
        if 'password' in request.POST:
            token = request.POST['password']
            if SecretToken.objects.filter(secret_token=token).exists():
                tg_id = SecretToken.objects.get(secret_token=token).telegram_id
                if not UserNameAndTelegramID.objects.filter(telegram_id=tg_id).exists():
                    UserNameAndTelegramID.objects.create(telegram_id=tg_id, customer=request.user)
            else:
                alert_text = 'Нет Телеграмм аккаунта с таким Секретным Токеном'
        else:
            UserNameAndTelegramID.objects.filter(customer=request.user).delete()
    usr = request.user.username
    flag = UserNameAndTelegramID.objects.filter(customer=usr).exists()
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
        RegistrationSite.objects.create(customer=self.request.POST['username'], email=self.request.POST['email'],
                                        data_registration=datetime.datetime.now().strftime('%d-%m-%Y'),
                                        blocked=False)
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
