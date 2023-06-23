from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path('', main, name='home'),

    path('info/', AllOlympiads, name='info'),
    path('info/<slug:sub_slug>/', FilterOlympiads, name='subject'),

    path('notification/', Notification, name='notification'),

    path('login/', LoginUser, name='login'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('logout/', logout_user, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
