from urllib.request import urlopen
from django.core.files.base import ContentFile
from .models import UserProfile 

def save_email(strategy, details, user=None, *args, **kwargs):
    """A pipeline step to save the user's email."""
    if user and details.get('email'):
        user.email = details['email']
        user.save()

def get_pfp(backend,user, strategy, details, response, is_new=False, *args, **kwargs):
    if not is_new:
        return
    if backend.name == 'facebook':
        url = f"http://graph.facebook.com/{response['id']}/picture?type=large"
    elif backend.name == 'google-oauth2' and "picture" in response:
        url = response['picture']
    else:
        return
    
    try:
        pfp = urlopen(url)
        if user.userprofile:
            profile = user.userprofile
        else:
            profile = UserProfile(user=user)
        
        profile.picture.save(f"{user.username}_social.jpg", ContentFile(pfp.read()))
        profile.save()
    except Exception as e:
        pass # Handle exception as needed
