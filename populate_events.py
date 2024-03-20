import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GEAARS.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event

def populate():
    events_data = [
        {'title': 'David Guetta', 'date': '2024-04-10', 'description': 'Renowned French DJ and producer, known for chart-topping electronic dance music hits and high-energy live performances.', 'location': 'Hydro', 'organizer_username': 'admin'},
        {'title': 'Maya Delilah', 'date': '2024-04-15', 'description': 'Emerging singer-songwriter captivating audiences with soulful melodies and poignant lyrics, blending indie-pop with R&B influences.', 'location': 'Bellahouston Park', 'organizer_username': 'admin'},
        {'title': 'Peach Pit', 'date': '2024-04-20', 'description': 'Indie rock band known for their laid-back, nostalgic sound, blending catchy melodies with witty lyrics and lo-fi aesthetics.', 'location': 'Barrowlands', 'organizer_username': 'admin'},
        {'title': 'Kevin Hart', 'date': '2024-04-25', 'description': 'Acclaimed comedian and actor, celebrated for his infectious humor, sharp wit, and standout performances in comedy specials and films.', 'location': 'King Tuts', 'organizer_username': 'admin'}
    ]

    for event_info in events_data:
        add_event(**event_info)

    for e in Event.objects.all():
        print(f'Event - {e.title}: {e.description}')

def add_event(title, date, description, location, organizer_username):
    organizer, created = User.objects.get_or_create(username=organizer_username)
    if created:
        organizer.set_password('defaultpassword')
        organizer.save()
    
    e, created = Event.objects.get_or_create(
        title=title,
        defaults={
            'description': description,
            'date': timezone.datetime.strptime(date, '%Y-%m-%d').date(),
            'location': location,
            'organizer': organizer
        }
    )
    return e

if __name__ == '__main__':
    print('Starting events population script...')
    populate()
