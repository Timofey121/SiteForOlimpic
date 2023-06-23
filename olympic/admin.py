from django.contrib import admin

from olympic.models import Registration, Olympiads, NotificationDates, Feedback, TechnicalSupport, Payment, Subjects, \
    SecretToken, UserNameAndTelegramID


# Register your models here.

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'full_name', 'blocked', 'data_registration')  # отображение этих в полей
    list_display_links = (
        'telegram_id', 'full_name', 'data_registration')  # кликабельные поля в админке, для перехода на запись в БД
    search_fields = ('full_name', 'telegram_id')  # поля, по которым можно искать записи
    list_editable = ('blocked',)  # поля, которые можно изменить, прямо в списке записей

    # поля, отображаемые в форме редактирования, некоторые не редактируемые
    fields = ('telegram_id', 'full_name', 'data_registration', 'blocked')


class OlympiadsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sub', 'title', 'start', 'stage', 'schedule', 'site', 'rsoch')  # отображение этих в полей
    list_display_links = ('id', 'title')  # кликабельные поля в админке, для перехода на запись в БД
    search_fields = ('sub', 'title')  # поля, по которым можно искать записи

    # поля, отображаемые в форме редактирования, некоторые не редактируемые
    fields = ('sub', 'title', 'start', 'stage', 'schedule', 'site', 'rsoch')


class NotificationDatesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sub', 'user', 'title', 'start', 'stage', 'schedule', 'site', 'rsoch')  # отображение этих в полей
    list_display_links = ('user', 'title')  # кликабельные поля в админке, для перехода на запись в БД
    search_fields = ('user', 'sub', 'title')  # поля, по которым можно искать записи
    list_editable = ('rsoch',)  # поля, которые можно изменить, прямо в списке записей

    # поля, отображаемые в форме редактирования, некоторые не редактируемые
    fields = ('sub', 'user', 'title', 'start', 'stage', 'schedule', 'site', 'rsoch')


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'feedback',)  # отображение этих в полей
    search_fields = ('user',)  # поля, по которым можно искать записи


class TechnicalSupportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'help',)  # отображение этих в полей
    search_fields = ('user',)  # поля, по которым можно искать записи


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'data',)  # отображение этих в полей
    search_fields = ('user',)  # поля, по которым можно искать записи


class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'slug', 'photo')  # отображение этих в полей
    search_fields = ('subject',)  # поля, по которым можно искать записи
    prepopulated_fields = {'slug': ("subject",)}  # автоматически заполнять поле slug на основе поля title


class SecretTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'secret_token',)  # отображение этих в полей
    list_display_links = ('telegram_id',)  # кликабельные поля в админке, для перехода на запись в БД
    search_fields = ('telegram_id',)  # поля, по которым можно искать записи


class UserNameAndTelegramIDAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'user',)  # отображение этих в полей
    list_display_links = ('telegram_id',)  # кликабельные поля в админке, для перехода на запись в БД
    search_fields = ('telegram_id', 'user')  # поля, по которым можно искать записи


admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Olympiads, OlympiadsAdmin)
admin.site.register(NotificationDates, NotificationDatesAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(TechnicalSupport, TechnicalSupportAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Subjects, SubjectsAdmin)
admin.site.register(SecretToken, SecretTokenAdmin)
admin.site.register(UserNameAndTelegramID, UserNameAndTelegramIDAdmin)
