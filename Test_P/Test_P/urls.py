from django.contrib import admin
from django.urls import path, include

from app_test import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("app_test.urls")),

]


handler404 = views.handler404
