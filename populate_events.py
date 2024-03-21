import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GEAARS.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event

def populate():
    events_data = [
        {'title': 'David Guetta', 'date': '2024-04-10', 'description': 'Renowned French DJ and producer, known for chart-topping electronic dance music hits and high-energy live performances.', 'location': 'SSE Hydro', 'organizer_username': 'admin'},
        {'title': 'Maya Delilah', 'date': '2024-04-15', 'description': 'Emerging singer-songwriter captivating audiences with soulful melodies and poignant lyrics, blending indie-pop with R&B influences.', 'location': 'Bellahouston Park', 'organizer_username': 'admin'},
        {'title': 'Peach Pit', 'date': '2024-04-20', 'description': 'Indie rock band known for their laid-back, nostalgic sound, blending catchy melodies with witty lyrics and lo-fi aesthetics.', 'location': 'Barrowlands', 'organizer_username': 'admin'},
        {'title': 'Kevin Hart', 'date': '2024-04-25', 'description': 'Acclaimed comedian and actor, celebrated for his infectious humor, sharp wit, and standout performances in comedy specials and films.', 'location': 'King Tuts', 'organizer_username': 'admin'},
        {'title': 'Kevin Bridges', 'date': '2018-12-07', 'description': 'Comedy superstar Kevin Bridges returns to the stage in 2018 with his sell out new show -- The Brand New Tour', 'location': 'SSE Hydro', 'organizer_username': 'admin'},
        {'title': 'Hella Mega Tour', 'date': '2022-06-29', 'description': 'The Hella Mega Tour is a worldwide concert tour by the band Green Day. The tour is also co-headlined by both Weezer and Fall Out Boy, all three of whom are playing their greatest hits and newest work', 'location': 'Bellahouston Park', 'organizer_username': 'admin'},
        {'title': 'Bongos Bingo', 'date': '2024-03-23', 'description': 'Its a crazy mix of traditional bingo, dance-offs, rave intervals, audience participation and countless magical moments.', 'location': 'SWG3', 'organizer_username': 'admin'},
        {'title': 'The Front Bottoms', 'date': '2023-12-11', 'description': 'The Front Bottoms are an American rock band from Woodcliff Lake, New Jersey.', 'location': 'O2 Academy', 'organizer_username': 'admin'},
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
