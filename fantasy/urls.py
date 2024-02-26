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
    path("league", views.league, name="league"),
    path("join-league", views.join_league, name="join_league"),
    path("new-league", views.new_league, name="new_league"),
    path("leave-league", views.leave_league, name="leave_league"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("save_prediction", views.save_prediction, name="save_prediction"),
    path("api/events", views.get_events, name="get_events"),
    path("api/predictions", views.get_predictions, name="get_predictions"),
    path("api/surfers", views.get_surfers, name="get_surfers"),
]
