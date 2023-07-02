from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginUserForm(AuthenticationForm):  # наследование от обычной аутентификации пользователей на сайте
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class SecretTokenForm(UserCreationForm):
    password = forms.CharField(label='Секретный Токен из Телеграмм Бота',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))


class PasswordReset(UserCreationForm):
    login_or_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(), max_length=100, initial='')
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')
