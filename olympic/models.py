from django.db import models
from django.urls import reverse


class RegistrationTelegram(models.Model):
    # id - PrimaryKey внесен в БД по умолчанию
    telegram_id = models.CharField(max_length=2000, verbose_name="Telegram id")
    full_name = models.CharField(max_length=2000, verbose_name="Имя пользователя")
    data_registration = models.CharField(max_length=2000, verbose_name="Дата регистрации")
    blocked = models.BooleanField(max_length=2000, verbose_name="Заблокирован ли?")

    # Тогда при выводе всех записей, для различия записей, будет отображаться их title
    def __str__(self):
        return self.full_name

    # Класс для работы с моделью в Админ-панели
    class Meta:
        verbose_name = 'Регистрация Телеграмм'  # название нашей модели в единственном числе
        verbose_name_plural = 'Регистрация Телеграм'  # название нашей модели во множественном числе
        ordering = ['full_name', '-data_registration']  # сортировка


class RegistrationSite(models.Model):
    # id - PrimaryKey внесен в БД по умолчанию
    user = models.CharField(max_length=2000, verbose_name="Имя пользователя")
    data_registration = models.CharField(max_length=2000, verbose_name="Дата регистрации")
    email = models.CharField(max_length=2000, verbose_name="E-mail", default=None)
    blocked = models.BooleanField(max_length=2000, verbose_name="Заблокирован ли?")

    # Тогда при выводе всех записей, для различия записей, будет отображаться их title
    def __str__(self):
        return self.user

    # Класс для работы с моделью в Админ-панели
    class Meta:
        verbose_name = 'Регистрация Сайт'  # название нашей модели в единственном числе
        verbose_name_plural = 'Регистрация Сайт'  # название нашей модели во множественном числе
        ordering = ['user', '-data_registration']  # сортировка


class ResetPassword(models.Model):
    # id - PrimaryKey внесен в БД по умолчанию
    user = models.CharField(max_length=2000, verbose_name="Имя пользователя")
    token = models.CharField(max_length=2000, verbose_name="Токен")
    data_created = models.DateField(auto_now_add=True, verbose_name="Время создания ссылки для сброса пароля")

    # Тогда при выводе всех записей, для различия записей, будет отображаться их title
    def __str__(self):
        return self.user

    # Класс для работы с моделью в Админ-панели
    class Meta:
        verbose_name = 'Сброс Пароля'  # название нашей модели в единственном числе
        verbose_name_plural = 'Сброс пароля'  # название нашей модели во множественном числе
        ordering = ['user']  # сортировка


class Olympiads(models.Model):
    title = models.CharField(max_length=2000, verbose_name="Название олимпиады")
    start = models.CharField(max_length=2000, verbose_name="Дата начала олимпиады")
    stage = models.CharField(max_length=2000, verbose_name="Этап олимпиады", default='None')
    schedule = models.CharField(max_length=2000, verbose_name="Расписание олимпиады", default='None')
    site = models.CharField(max_length=2000, verbose_name="Сайт олимпиады", default='None')
    rsoch = models.BooleanField(max_length=2000, verbose_name="Входит ли в перечень?")

    sub = models.ForeignKey('Subjects', on_delete=models.PROTECT, verbose_name="Предмет")

    # Тогда при выводе всех записей, для различия записей, будет отображаться их title
    def __str__(self):
        return self.title

    # Класс для работы с моделью в Админ-панели
    class Meta:
        verbose_name = 'Олимпиада'  # название нашей модели в единственном числе
        verbose_name_plural = 'Олимпиады'  # название нашей модели во множественном числе
        ordering = ['sub', 'start']  # сортировка


class NotificationDates(models.Model):
    user = models.CharField(max_length=2000, verbose_name="Пользователь или его Telegram_ID")

    title = models.CharField(max_length=2000, verbose_name="Название олимпиады")
    start = models.CharField(max_length=2000, verbose_name="Дата начала олимпиады")
    stage = models.CharField(max_length=2000, verbose_name="Этап олимпиады", default='None')
    schedule = models.CharField(max_length=2000, verbose_name="Расписание олимпиады", default='None')
    site = models.CharField(max_length=2000, verbose_name="Сайт олимпиады", default='None')

    rsoch = models.BooleanField(max_length=2000, verbose_name="Входит ли в перечень?")

    sub = models.ForeignKey('Subjects', on_delete=models.PROTECT, verbose_name="Предмет")

    # Тогда при выводе всех записей, для различия записей, будет отображаться их title
    def __str__(self):
        return self.title

    # Класс для работы с моделью в Админ-панели
    class Meta:
        verbose_name = 'Подключенное уведомление'  # название нашей модели в единственном числе
        verbose_name_plural = 'Подключенные уведомления'  # название нашей модели во множественном числе
        ordering = ['user', 'start']  # сортировка


class Subjects(models.Model):
    subject = models.CharField(max_length=2000, verbose_name="Предмет")
    slug = models.SlugField(max_length=2000, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to="subjects/", verbose_name="Фото")

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('subject', kwargs={'sub_slug': self.slug})

    class Meta:
        verbose_name = 'Предмет'  # название нашей модели в единственном числе
        verbose_name_plural = 'Предметы'  # название нашей модели во множественном числе
        ordering = ['subject']  # сортировка


class SecretToken(models.Model):
    # id - PrimaryKey внесен в БД по умолчанию
    telegram_id = models.CharField(max_length=2000, verbose_name="Telegram id")
    secret_token = models.CharField(max_length=2000, verbose_name="Секретный Токен")

    # Тогда при выводе всех записей, для различия записей, будет отображаться их title
    def __str__(self):
        return self.telegram_id

    # Класс для работы с моделью в Админ-панели
    class Meta:
        verbose_name = 'Секретный Токен'  # название нашей модели в единственном числе
        verbose_name_plural = 'Секретные Токены'  # название нашей модели во множественном числе
        ordering = ['telegram_id', ]  # сортировка


class UserNameAndTelegramID(models.Model):
    telegram_id = models.CharField(max_length=2000, verbose_name="Telegram id")
    user = models.CharField(max_length=2000, verbose_name="Пользователь")

    # Тогда при выводе всех записей, для различия записей, будет отображаться их title
    def __str__(self):
        return self.telegram_id

    # Класс для работы с моделью в Админ-панели
    class Meta:
        verbose_name = 'Соединение Телеграмм и Сайта'  # название нашей модели в единственном числе
        verbose_name_plural = 'Соединение Телеграмм и Сайта'  # название нашей модели во множественном числе
        ordering = ['telegram_id', ]  # сортировка


class Feedback(models.Model):
    # id - PrimaryKey внесен в БД по умолчанию
    user = models.CharField(max_length=2000, verbose_name="Telegram id")
    feedback = models.CharField(max_length=2000, verbose_name="Обратная связь")

    # Тогда при выводе всех записей, для различия записей, будет отображаться их title
    def __str__(self):
        return self.user

    # Класс для работы с моделью в Админ-панели
    class Meta:
        verbose_name = 'Отзыв'  # название нашей модели в единственном числе
        verbose_name_plural = 'Отзывы'  # название нашей модели во множественном числе
        ordering = ['user']  # сортировка


class TechnicalSupport(models.Model):
    # id - PrimaryKey внесен в БД по умолчанию
    user = models.CharField(max_length=2000, verbose_name="Telegram id")
    help = models.CharField(max_length=2000, verbose_name="Обращение")

    # Тогда при выводе всех записей, для различия записей, будет отображаться их title
    def __str__(self):
        return self.user

    # Класс для работы с моделью в Админ-панели
    class Meta:
        verbose_name = 'Обращение в помощь'  # название нашей модели в единственном числе
        verbose_name_plural = 'Обращения в помощь'  # название нашей модели во множественном числе
        ordering = ['user', 'help']  # сортировка


class Payment(models.Model):
    # id - PrimaryKey внесен в БД по умолчанию
    user = models.CharField(max_length=2000, verbose_name="Telegram id")
    data = models.CharField(max_length=2000, verbose_name="Обращение")

    # Тогда при выводе всех записей, для различия записей, будет отображаться их title
    def __str__(self):
        return self.user

    # Класс для работы с моделью в Админ-панели
    class Meta:
        verbose_name = 'Оплата'  # название нашей модели в единственном числе
        verbose_name_plural = 'Оплата'  # название нашей модели во множественном числе
        ordering = ['user', 'data']  # сортировка
