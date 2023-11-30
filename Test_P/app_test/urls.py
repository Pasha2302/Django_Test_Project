# chat/urls.py
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, re_path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/profile/', views.profile_view, name='profile'),
    path("slots/<slug:slug_slot>", views.one_slot, name="one_slot"),

    path(r"test_paginator/slots", views.SlotsListView.as_view(), name="slots_list"),

    path("load_more", views.load_more, name="load_more"),
    path("test_scroll", views.test_scroll, name="test_scroll"),

    path('login/', views.CustomLoginView.as_view(), name='login'),
]


# Добавление URL-паттернов для обслуживания статических файлов в отладочном режиме
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)