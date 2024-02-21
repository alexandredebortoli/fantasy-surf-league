from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("events", views.events, name="events"),
    path("rankings", views.rankings, name="rankings"),
    path("surfers", views.surfers, name="surfers"),
]
