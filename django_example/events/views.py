from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .dispatcher import EventsDispatcher
from .models import User, Event


def signup(request):
    if not request.POST:
        return render(request, "events/signup.html")

    username = request.POST["username"]
    password = request.POST["password"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    birthdate = request.POST["birthdate"]

    if not username:
        messages.error(request, f"Поле 'Имя пользователя' не может быть пустым")
        return redirect("/signup")
    if not password:
        messages.error(request, f"Поле 'Пароль' не может быть пустым")
        return redirect("/signup")
    if not first_name:
        messages.error(request, f"Поле 'Имя' не может быть пустым")
        return redirect("/signup")
    if not last_name:
        messages.error(request, f"Поле 'Фамилия' не может быть пустым")
        return redirect("/signup")
    if not birthdate:
        birthdate = None

    try:
        EventsDispatcher.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate
        )
    except EventsDispatcher.Error as e:
        messages.error(request, str(e))
        return redirect("/signup")
    else:
        django_user = authenticate(request, username=username, password=password)
        django_login(request, django_user)
        return redirect("/events")


def login(request):
    if not request.POST:
        return render(request, "events/login.html")

    username = request.POST["username"]
    password = request.POST["password"]

    if not EventsDispatcher.is_username_taken(request.POST["username"]):
        messages.error(request, f"Пользователя {username} не существует")
        return redirect("/login")

    django_user = authenticate(request, username=username, password=password)

    if django_user is None:
        messages.error(request, f"Неверный пароль")
        return redirect("/login")

    django_login(request, django_user)
    return redirect("/events")


def logout(request):
    django_logout(request)
    return redirect("/login")


@login_required(login_url="/login")
def index(request):
    return redirect("/events")


@login_required(login_url="/login")
def events(request):
    current_user = EventsDispatcher.get_current_user(request.user)
    context = {
        "current_user": current_user,
        "all_events": EventsDispatcher.get_events(),
        "user_events": EventsDispatcher.get_events(user_id=current_user.id)
    }
    return render(request, "events/index.html", context)


@login_required(login_url="/login")
def user(request, user_id: int):
    current_user = EventsDispatcher.get_current_user(request.user)
    context = {
        "current_user": current_user,
        "user": User.objects.get(id=user_id)
    }
    return render(request, "events/user.html", context)


@login_required(login_url="/login")
def event(request, event_id: int):
    current_user = EventsDispatcher.get_current_user(request.user)
    context = {
        "current_user": current_user,
        "all_events": EventsDispatcher.get_events(),
        "user_events": EventsDispatcher.get_events(user_id=current_user.id),
        "event": Event.objects.get(id=event_id)
    }
    return render(request, "events/event.html", context)


@login_required(login_url="/login")
def participate_event(request, event_id: int):
    current_user = EventsDispatcher.get_current_user(request.user)
    event = Event.objects.get(id=event_id)
    EventsDispatcher.add_participant(event, current_user)
    return redirect(f"/events/{event_id}/")


@login_required(login_url="/login")
def exit_event(request, event_id: int):
    current_user = EventsDispatcher.get_current_user(request.user)
    event = Event.objects.get(id=event_id)
    EventsDispatcher.remove_participant(event, current_user)
    return redirect(f"/events/{event_id}/")
