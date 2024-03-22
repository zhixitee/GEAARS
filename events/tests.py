from django.test import TestCase
from django.urls import reverse, resolve
from .views import events
from .forms import EventForm 

class EventModelTest(TestCase):
    def setUp(self):
        events.objects.create(title="Test Event", description="Just a test event")

    def test_event_creation(self):
        event = events.objects.get(title="Test Event")
        self.assertEqual(event.description, "Just a test event")

class EventViewTest(TestCase):
    def test_event_list_url_is_resolved(self):
        url = reverse('your_correct_event_list_view_name')
        self.assertEquals(resolve(url).func, events)

    def test_event_form_with_valid_data(self):
        form_data = {
            'title': 'Test Event',
            'date': '2022-12-31',
            'location': 'Test Location',
            'description': 'Test Description',
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

class EventFormTest(TestCase):
    def test_valid_data(self):
        form = EventForm({
            'title': "New Event",
            'description': "Another test event",
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = EventForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
