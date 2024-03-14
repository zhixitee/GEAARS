
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Event, UserEvent
from .forms import EventForm, UserForm, UserProfileForm


def events(request):
    all_events = Event.objects.all()
    return render(request, 'events/events.html', {'events': all_events})


def choosenEvent(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    return render(request, 'events/choosenEvent.html', {'event': event})


def about(request):
    visitor_cookie_handler(request)
    return render(request, 'events/about.html')


def map(request):
    return render(request, 'events/map.html')


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('events:events')
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('events:events')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'events/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('events:events')
            else:
                return HttpResponse("Your account has been disabled.")
        else:
            return HttpResponse("Invalid login details.")
    else:
        return render(request, 'events/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('events:events')


@login_required
def user_events_list(request):
    user_events = UserEvent.objects.filter(user=request.user)
    return render(request, 'events/user_events_list.html', {'user_events': user_events})


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(
        request, 'last_visit', str(timezone.now()))

    # Ensure last_visit_time is timezone-aware
    last_visit_time = timezone.datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=timezone.utc)

    if (timezone.now() - last_visit_time).days > 0:
        visits += 1
        # Save the new visit information
        request.session['last_visit'] = str(timezone.now())
    else:
        # Otherwise, use the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits
