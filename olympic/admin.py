from django.contrib import admin

from olympic.models import RegistrationSite, RegistrationTelegram, Olympiads, NotificationDates, Feedback, \
    TechnicalSupport, Payment, \
    Subjects, SecretToken, UserNameAndTelegramID, ResetPassword


# Register your models here.

class RegistrationSiteAdmin(admin.ModelAdmin):
    list_display = ('customer', 'email', 'blocked', 'data_registration')  # отображение этих в полей
    list_display_links = (
        'customer', 'email', 'data_registration')  # кликабельные поля в админке, для перехода на запись в БД
    search_fields = ('email', 'customer')  # поля, по которым можно искать записи
    list_editable = ('blocked',)  # поля, которые можно изменить, прямо в списке записей

    # поля, отображаемые в форме редактирования, некоторые не редактируемые
    fields = ('customer', 'email', 'data_registration', 'blocked')


class RegistrationTelegramAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'full_name', 'blocked', 'data_registration')  # отображение этих в полей
    list_display_links = (
        'telegram_id', 'full_name', 'data_registration')  # кликабельные поля в админке, для перехода на запись в БД
    search_fields = ('full_name', 'telegram_id')  # поля, по которым можно искать записи
    list_editable = ('blocked',)  # поля, которые можно изменить, прямо в списке записей

    # поля, отображаемые в форме редактирования, некоторые не редактируемые
    fields = ('telegram_id', 'full_name', 'data_registration', 'blocked')


class OlympiadsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sub', 'title', 'start', 'stage', 'rsoch')  # отображение этих в полей
    list_display_links = ('id', 'title')  # кликабельные поля в админке, для перехода на запись в БД
    list_editable = ('rsoch',)  # поля, которые можно изменить, прямо в списке записей
    search_fields = ('sub', 'title')  # поля, по которым можно искать записи

    # поля, отображаемые в форме редактирования, некоторые не редактируемые
    fields = ('sub', 'title', 'start', 'stage', 'schedule', 'site', 'rsoch')


class NotificationDatesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sub', 'customer', 'title', 'start', 'stage', 'rsoch')  # отображение этих в полей
    list_display_links = ('customer', 'title')  # кликабельные поля в админке, для перехода на запись в БД
    search_fields = ('customer', 'sub', 'title')  # поля, по которым можно искать записи
    list_editable = ('rsoch',)  # поля, которые можно изменить, прямо в списке записей

    # поля, отображаемые в форме редактирования, некоторые не редактируемые
    fields = ('sub', 'customer', 'title', 'start', 'stage', 'schedule', 'site', 'rsoch')


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'feedback',)  # отображение этих в полей
    search_fields = ('customer',)  # поля, по которым можно искать записи


class TechnicalSupportAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'help',)  # отображение этих в полей
    search_fields = ('customer',)  # поля, по которым можно искать записи


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'data',)  # отображение этих в полей
    search_fields = ('customer',)  # поля, по которым можно искать записи


class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'slug', 'photo')  # отображение этих в полей
    search_fields = ('subject',)  # поля, по которым можно искать записи
    prepopulated_fields = {'slug': ("subject",)}  # автоматически заполнять поле slug на основе поля title


class SecretTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'secret_token',)  # отображение этих в полей
    list_display_links = ('telegram_id',)  # кликабельные поля в админке, для перехода на запись в БД
    search_fields = ('telegram_id',)  # поля, по которым можно искать записи


class ResetPasswordAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'token', 'data_created')  # отображение этих в полей
    list_display_links = ('customer',)  # кликабельные поля в админке, для перехода на запись в БД
    search_fields = ('customer',)  # поля, по которым можно искать записи
    fields = ('customer', 'token', 'data_created')


class UserNameAndTelegramIDAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'customer',)  # отображение этих в полей
    list_display_links = ('telegram_id',)  # кликабельные поля в админке, для перехода на запись в БД
    search_fields = ('telegram_id', 'customer')  # поля, по которым можно искать записи


admin.site.register(RegistrationSite, RegistrationSiteAdmin)
admin.site.register(RegistrationTelegram, RegistrationTelegramAdmin)
admin.site.register(Olympiads, OlympiadsAdmin)
admin.site.register(ResetPassword, ResetPasswordAdmin)
admin.site.register(NotificationDates, NotificationDatesAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(TechnicalSupport, TechnicalSupportAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Subjects, SubjectsAdmin)
admin.site.register(SecretToken, SecretTokenAdmin)
admin.site.register(UserNameAndTelegramID, UserNameAndTelegramIDAdmin)
