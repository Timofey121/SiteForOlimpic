from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path('', main, name='home'),

    path('info/', AllOlympiads, name='info'),
    path('info/<slug:sub_slug>/', FilterOlympiads, name='subject'),

    path('notification/', Notification, name='notification'),

    path('SecretToken/', token, name='secret_token'),
    path('login/', LoginUser.as_view(), name='login'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('logout/', logout_user, name='logout'),
    path('password_reset/', password_reset, name='password_reset'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
