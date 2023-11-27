# chat/urls.py
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("filters/", views.room, name="room"),
    path("slots/<slug:slug_slot>/", views.one_slot, name="one_slot"),
]


# Добавление URL-паттернов для обслуживания статических файлов в отладочном режиме
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)