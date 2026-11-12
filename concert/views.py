import os

import requests
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import LoginForm, SignUpForm
from .models import Concert, ConcertAttending


def signup(request):
    form = SignUpForm(request, data=request.POST or None)
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        if username and len(username) <= 100 and 3 <= len(password) <= 50:
            try:
                user = User.objects.create_user(username=username, password=password)
            except IntegrityError:
                form.add_error("username", "This username is already registered.")
            else:
                login(request, user)
                return redirect("index")
        else:
            form.add_error(None, "Enter a username and a valid password.")
    return render(request, "signup.html", {"form": form})


def index(request):
    return render(request, "index.html")


def service_page(request, variable, default, endpoint, template, key):
    try:
        response = requests.get(os.getenv(variable, default).rstrip("/") + endpoint, timeout=5)
        response.raise_for_status()
        records = response.json()
        if isinstance(records, dict):
            records = records.get(key)
        if not isinstance(records, list):
            raise ValueError("Expected a list of records")
    except (requests.RequestException, ValueError):
        return render(request, template, {key: []}, status=503)
    return render(request, template, {key: records})


def songs(request):
    return service_page(request, "SONGS_URL", "http://127.0.0.1:5001", "/song", "songs.html", "songs")


def photos(request):
    return service_page(request, "PICTURES_URL", "http://127.0.0.1:5000", "/picture", "photos.html", "photos")


def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("index")
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")


@login_required(login_url="login")
def concerts(request):
    attendance = dict(ConcertAttending.objects.filter(user=request.user).values_list("concert_id", "attending"))
    rows = [{"concert": concert, "status": attendance.get(concert.pk, "-")} for concert in Concert.objects.order_by("date", "pk")]
    return render(request, "concerts.html", {"concerts": rows})


@login_required(login_url="login")
def concert_detail(request, id):
    concert = get_object_or_404(Concert, pk=id)
    record = concert.attendee.filter(user=request.user).first()
    return render(request, "concert_detail.html", {
        "concert_details": concert,
        "status": record.attending if record else "-",
        "attending_choices": ConcertAttending.AttendingChoices.choices,
    })


@login_required(login_url="login")
@require_POST
def concert_attendee(request):
    concert = get_object_or_404(Concert, pk=request.POST.get("concert_id"))
    choice = request.POST.get("attendee_choice")
    if choice in ConcertAttending.AttendingChoices.values:
        ConcertAttending.objects.update_or_create(
            concert=concert, user=request.user, defaults={"attending": choice}
        )
    return redirect("concerts")
