from events.models import Event, User, UserEvent
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GEAARS.settings')
django.setup()

def populate_user_events():
    user_events_data = [
        {'event_id': 1, 'user_id': 1},  # Adjust IDs based on your actual Event and User records
        {'event_id': 2, 'user_id': 2},
    ]

    for data in user_events_data:
        event = Event.objects.get(pk=data['event_id'])  # Ensure the Event exists
        user = User.objects.get(pk=data['user_id'])    # Ensure the User exists
        UserEvent.objects.get_or_create(user=user, event=event)

    for user_event in UserEvent.objects.all():
        print(user_event)

if __name__ == '__main__':
    print('Starting user events population script...')
    populate_user_events()
