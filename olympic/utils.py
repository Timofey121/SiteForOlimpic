menu = [{'title': "Главная страница", 'url_name': 'home'},
        {'title': "Информация об олимпиадах", 'url_name': 'info'},
        ]

additional_menu = [
    {'title': "Подключение/Удаление уведомлений", 'url_name': 'notification'},
]


class DataMixin:  # убираем дублирование кода
    # paginate_by = 2  # В класс ListView встроена пагинация, paginate_by = сколько записей на одной странице отображать

    def get_user_context(self, **kwargs):  # создаем нужный контекст по умолчанию
        context = kwargs
        user_menu = menu.copy()
        if self.request.user.is_authenticated:
            user_menu += additional_menu.copy()
        context['menu'] = user_menu  # создан контекст для меню
        return context
