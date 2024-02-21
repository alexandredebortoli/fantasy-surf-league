from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.cache import cache_page

from fantasy.models import User
from fantasy.webscraper import scrape_events_schedule


def index(request):
    return render(request, "pages/index.html")


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "pages/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "pages/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "pages/register.html", {"message": "Passwords must match."}
            )

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as error:
            message = "Failed to create account. Try again later."
            if "UNIQUE constraint" in str(error) and "username" in str(error):
                message = "Username already taken."
            elif "UNIQUE constraint" in str(error) and "email" in str(error):
                message = "Email already taken."
            return render(
                request,
                "pages/register.html",
                {"message": message},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "pages/register.html")


@cache_page(60 * 60 * 24)
def events(request):
    events = scrape_events_schedule()
    return render(request, "pages/events.html", {"events": events})


def rankings(request):
    return render(request, "pages/rankings.html")


def surfers(request):
    events = scrape_events_schedule()
    return render(request, "pages/surfers.html")
