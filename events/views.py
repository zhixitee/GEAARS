from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from events.forms import EventForm, UserForm, UserProfileForm
from events.models import Category, Event, UserEvent, EventReview, CommentReview
from events.forms import CategoryForm, UserForm, UserProfileForm, EventReviewForm, CommentForm
from datetime import datetime
import json
from django.contrib import messages
from django.db.models import Q


def events(request):
    query = request.GET.get('q')
    if query:
        all_events = Event.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    else:
        all_events = Event.objects.all()
    return render(request, 'events/events.html', {'events': all_events, 'show_search_bar': True})


@login_required
def make_a_review_discuss_event(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    
    if event.date > timezone.now():
        messages.error(request, "You cannot review an event before it has occurred.")
        return redirect('events:choosen_event', event_slug=event.slug)
   
    if request.method == 'POST':
        review_form = EventReviewForm(request.POST, prefix="review")
        comment_form = CommentForm(request.POST, prefix="comment")

        if review_form.is_valid() and comment_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.event = event
            review.save()

            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.event = event
            comment.save()

            messages.success(request, 'Submitted successfully!')
            return redirect('events:choosen_event', event_slug=event.slug)
        else:
            messages.error(
                request, 'Error submitting your review and comment. Please check for errors.')
    else:
        review_form = EventReviewForm(prefix="review")
        comment_form = CommentForm(prefix="comment")

    context = {
        'now': timezone.now(),
        'event': event,
        'review_form': review_form,
        'comment_form': comment_form,
    }
    return render(request, 'events/choosenEvent.html', context)


def choosenEvent(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    review_form = EventReviewForm(prefix="review")
    comment_form = CommentForm(prefix="comment")

    comments = CommentReview.objects.filter(event=event)

    context = {
        'event': event,
        'review_form': review_form,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'events/choosenEvent.html', context)


def about(request):
    visitor_cookie_handler(request)
    return render(request, 'events/about.html', {'show_search_bar': True})


def map(request):
    venues = [
        {"name": "King Tut's Wah Wah Hut", "lat": 55.8625967562286, "lng": -4.264986115540963,
            "info": "Mighty concert room for up-and-coming local bands and cult international acts serving own lager. Address: 272A St Vincent St, Glasgow G2 5RL Phone: 0141 846 4034."},
        {"name": "OVO Hydro", "lat": 55.85972303446611, "lng": -4.285458255827642,
            "info": "Multi-purpose indoor arena located within the Scottish Event Campus. Address: Exhibition Way, Stobcross Rd, Glasgow G3 8YW Capacity: 12,306 (all seated); 14,500 (with standing) Phone: 0141 248 3000"},
        {"name": "Barrowland Ballroom", "lat": 55.85536512400785, "lng": -4.236643115351418,
            "info": "Entertainment venue, dance hall and music venue located in the Calton district. Address: 244 Gallowgate, Glasgow G4 0TT Capacity: 1,900 Phone: 0141 552 4601"},
        {"name": "Bellahouston Park", "lat": 55.84642667620242, "lng": -4.313516156358837,
            "info": "A public park in the Bellahouston district on the South Side of Glasgow. Address: 16 Dumbreck Rd, Bellahouston, Glasgow G41 5BW Phone: 0141 287 9700"}
    ]
    venues_json = json.dumps(venues)
    return render(request, 'events/map.html', {'venues_json': venues_json})


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
    last_visit_time = timezone.datetime.strptime(
        last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=timezone.utc)

    if (timezone.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(timezone.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits
