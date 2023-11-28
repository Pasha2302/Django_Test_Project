# chat/urls.py
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/profile/', views.profile_view, name='profile'),
    path("slots/<slug:slug_slot>/", views.one_slot, name="one_slot"),
    path("test_paginator/", views.one_slot, name="one_slot"),

    path('login/', views.CustomLoginView.as_view(), name='login'),
]


# Добавление URL-паттернов для обслуживания статических файлов в отладочном режиме
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)