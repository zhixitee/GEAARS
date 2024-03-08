import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GEAARS.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Category, Page, Event

def populate():
    # Define your categories and events data
    python_events = [
        {'title': 'PyCon', 'date': timezone.now(), 'description': 'Annual conference for the Python community.', 'location': 'Online', 'organizer_username': 'admin'},
        {'title': 'DjangoCon', 'date': timezone.now(), 'description': 'Conference for Django developers.', 'location': 'Online', 'organizer_username': 'admin'},
    ]

    python_cat = add_cat('Python', 128, 64)

    for event_info in python_events:
        add_event(python_cat, **event_info)

    for c in Category.objects.all():
        print(f'Category - {c}:')
        for e in Event.objects.all():  # Modified as Events are not linked to Categories directly
            print(f'- {e.title}: {e.description}')

def add_event(cat, title, date, description, location, organizer_username):
    # Create the organizer user if not exists
    organizer, created = User.objects.get_or_create(username=organizer_username)
    if created:
        organizer.set_password('defaultpassword')  # Set a default password or another method
        organizer.save()
    
    # Then create the event
    e, created = Event.objects.get_or_create(
        title=title,
        defaults={
            'description': description,
            'date': date,
            'location': location,
            'organizer': organizer
        }
    )
    return e


def add_cat(name, views=0, likes=0):
    c, created = Category.objects.get_or_create(name=name)
    if created:
        c.views = views
        c.likes = likes
        c.save()
    return c

if __name__ == '__main__':
    print('Starting events population script...')
    populate()
