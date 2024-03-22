from django import forms
from django.contrib.auth.models import User
from .models import Category, UserProfile, Event, CommentReview, EventReview, UserFeedback,Feedback

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH,
                        help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'organizer']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentReview
        fields = ['content']


class EventReviewForm(forms.ModelForm):
    class Meta:
        model = EventReview
        fields = ['atmosphere_rating', 'concession_price_rating', 'artist_rating', 'value_rating', 'location_rating']
        widgets = {
            'atmosphere_rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'concession_price_rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'artist_rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'value_rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'location_rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }

class UserFeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ['review']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['category', 'message']