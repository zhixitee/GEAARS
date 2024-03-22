from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from events.forms import EventForm, UserForm, UserProfileForm
from events.models import Category, Event, UserEvent, EventReview, CommentReview, UserProfile
from events.forms import CategoryForm, UserForm, UserProfileForm, EventReviewForm, CommentForm
from datetime import datetime
from django.contrib import messages
from .forms import UserFeedbackForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import transaction


def events(request):
    query = request.GET.get('q')
    order_by = request.GET.get('order_by', 'date_desc')  # Default to newest first
    events_query = Event.objects.all()

    if query:
        events_query = events_query.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    
    # Adjust ordering based on the selection
    if order_by == 'date_desc':
        events_query = events_query.order_by('-date')
    elif order_by == 'date_asc':
        events_query = events_query.order_by('date')

    return render(request, 'events/events.html', {
        'events': events_query,
        'show_search_bar': True,
    })


@login_required
def make_a_review_discuss_event(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    
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
        'event': event,
        'review_form': review_form,
        'comment_form': comment_form,
    }
    return render(request, 'events/choosenEvent.html', context)



def choosenEvent(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    review_form = EventReviewForm(prefix="review")
    comment_form = CommentForm(prefix="comment")
    event_has_occurred = event.date < timezone.now()
    comments = CommentReview.objects.filter(event=event)

    context = {
        'event': event,
        'review_form': review_form,
        'comment_form': comment_form,
        'comments': comments,
        'event_has_occurred': event_has_occurred,
    }
    return render(request, 'events/choosenEvent.html', context)


def about(request):
    visitor_cookie_handler(request)
    return render(request, 'events/about.html', {'show_search_bar': True})


def map(request):
    events = Event.objects.filter(date__gt=timezone.now())
    return render(request, 'events/map.html', {'events': events})


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
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()

            user = authenticate(username=user.username, password=user_form.cleaned_data['password'])
            if user:
                login(request, user)
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

@login_required
def submit_user_feedback(request):
    if request.method == 'POST':
        form = UserFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback_thank_you')  
    else:
        form = UserFeedbackForm()
    return render(request, 'feedback.html', {'form': form})
