from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.serializers import serialize
import json

from fantasy.models import *
from fantasy.task import scrape_and_update_data
from fantasy.webscraper import (
    scrape_rankings,
)


def index(request):
    scrape_and_update_data()
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


def events(request):
    events = Event.objects.all()
    return render(request, "pages/events.html", {"events": events})


def rankings(request):
    rankings = Ranking.objects.all().order_by("rank")
    return render(request, "pages/rankings.html", {"rankings": rankings})


def surfers(request):
    surfers = Surfer.objects.all()
    return render(request, "pages/surfers.html", {"surfers": surfers})


def league(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user = User.objects.get(pk=request.user.id)
    if user.league:
        league = League.objects.get(pk=user.league.id)
        league_members = league.members.all()
        leaderboard = []
        for league_member in league_members:
            total_points = Prediction.objects.total_points_for_user(league_member)
            if not total_points:
                total_points = 0
            leaderboard.append((total_points, league_member))
        leaderboard.sort(key=lambda x: x[0], reverse=True)
        leaderboard = [
            ((index + 1), total_points, member)
            for index, (total_points, member) in enumerate(leaderboard)
        ]
        return render(
            request, "pages/league.html", {"league": league, "leaderboard": leaderboard}
        )
    return render(request, "pages/league.html")


def join_league(request):
    if request.method == "POST":
        code = request.POST["code"]
        author = request.user
        league = League.objects.get(identifier=code)
        if not league:
            return render(
                request,
                "pages/league.html",
                {"message": "League not found."},
            )

        author.league = league
        author.save()

    return HttpResponseRedirect(reverse("league"))


def new_league(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        author = User.objects.get(pk=request.user.id)
        league = League(name=name, description=description, creator=author)
        league.save()
        author.league = league
        author.save()

    return HttpResponseRedirect(reverse("league"))


def leave_league(request):
    if request.method == "POST":
        author = User.objects.get(pk=request.user.id)
        league = League.objects.get(pk=author.league.id)
        if league.creator == author:
            league.delete()
        author.league = None
        author.save()

    return HttpResponseRedirect(reverse("league"))


def profile(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    profile_user = User.objects.get(username=username)
    total_points = total_points = Prediction.objects.total_points_for_user(profile_user)
    if not total_points:
        total_points = 0
    join_date = profile_user.date_joined.strftime("%b %d, %Y")
    first_event = Event.objects.get(number=1)
    surfers = Surfer.objects.all()
    try:
        first_event_prediction = Prediction.objects.get(
            user=profile_user, event=first_event
        )
    except:
        first_event_prediction = None

    return render(
        request,
        "pages/profile.html",
        {
            "profile_user": profile_user,
            "total_points": total_points,
            "join_date": join_date,
            "event_range": range(1, 11),
            "event": first_event,
            "surfers": surfers,
            "prediction": first_event_prediction,
        },
    )


def save_prediction(request):
    return HttpResponseRedirect(reverse("profile", args=(request.user.username,)))


def get_events(request):
    events = Event.objects.all()
    serialized_data = serialize("json", events)
    serialized_data = json.loads(serialized_data)
    serialized_data
    return JsonResponse(serialized_data, safe=False, status=200)


def get_predictions(request):
    predictions = Prediction.objects.filter(user=request.user)
    serialized_data = serialize("json", predictions)
    serialized_data = json.loads(serialized_data)
    serialized_data
    return JsonResponse(serialized_data, safe=False, status=200)


def get_surfers(request):
    surfers = Surfer.objects.all()
    serialized_data = serialize("json", surfers)
    serialized_data = json.loads(serialized_data)
    serialized_data
    return JsonResponse(serialized_data, safe=False, status=200)
