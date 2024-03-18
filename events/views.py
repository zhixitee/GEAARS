from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from events.forms import EventForm, UserForm, UserProfileForm
from events.models import Category, Page, Event, UserEvent
from events.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime
import json

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
    venues = [
        {"name": "King Tut's Wah Wah Hut", "lat": 55.8625967562286, "lng": -4.264986115540963, "info": "Mighty concert room for up-and-coming local bands and cult international acts serving own lager. Address: 272A St Vincent St, Glasgow G2 5RL Phone: 0141 846 4034."},
        {"name": "OVO Hydro", "lat": 55.85972303446611, "lng": -4.285458255827642, "info": "Multi-purpose indoor arena located within the Scottish Event Campus. Address: Exhibition Way, Stobcross Rd, Glasgow G3 8YW Capacity: 12,306 (all seated); 14,500 (with standing) Phone: 0141 248 3000"},
        {"name": "Barrowland Ballroom", "lat": 55.85536512400785, "lng": -4.236643115351418, "info": "Entertainment venue, dance hall and music venue located in the Calton district. Address: 244 Gallowgate, Glasgow G4 0TT Capacity: 1,900 Phone: 0141 552 4601"},
        {"name": "Bellahouston Park", "lat": 55.84642667620242, "lng": -4.313516156358837, "info": "A public park in the Bellahouston district on the South Side of Glasgow. Address: 16 Dumbreck Rd, Bellahouston, Glasgow G41 5BW Phone: 0141 287 9700"}
    ]
    venues_json = json.dumps(venues)
    return render(request, 'map.html', {'venues_json': venues_json})

def choosenEvent(Request):
    return render(Request, 'events/choosenEvent.html')

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    
    return render(request, 'events/category.html', context=context_dict)

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
