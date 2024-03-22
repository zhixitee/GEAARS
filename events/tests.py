from django.test import TestCase
from django.urls import reverse, resolve
from .views import events
from .models import Event, EventReview
from .forms import EventForm 
from django.contrib.auth.models import User
from django.utils import timezone


class EventModelTest(TestCase):
    def setUp(self):
        Event.objects.create(title="Test Event", description="Just a test event")

    def test_event_creation(self):
        event = Event.objects.get(title="Test Event")
        self.assertEqual(event.description, "Just a test event")

class EventViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='admin', password='12345')
        cls.event = Event.objects.create(
            title="Admin's Event",
            description="Event created by admin",
            date=timezone.now() + timezone.timedelta(days=10),
            location="Admin's Location",
            organizer=cls.user
        )

    def test_events_view_exists_at_desired_location(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)

    def test_events_view_uses_correct_template(self):
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/events.html')

    # def test_events_view_lists_events(self):
    #     response = self.client.get(reverse('events')) 
    #     self.assertEqual(response.status_code, 200, "The events page did not load correctly")
    #     self.assertContains(response, "Admin&#39;s Event", html=True, msg_prefix="Event title not found in the response")


class EventFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def test_valid_data(self):
        form_data = {
            'title': "New Event",
            'description': "Another test event",
            'date': timezone.now(), 
            'location': "Some Location",
            'organizer': self.user.id, 
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = EventForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5) 
