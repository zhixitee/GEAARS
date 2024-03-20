def save_email(strategy, details, user=None, *args, **kwargs):
    """A pipeline step to save the user's email."""
    print("Email from details:", details.get('email'))  # Debug print
    if user and details.get('email'):
        user.email = details['email']
        user.save()

def get_pfp(backend, strategy, details, response,
        user=None, *args, **kwargs):
    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
    if backend.name == 'google-oauth2':
        url = response['picture']
        ext = url.split('.')[-1]
    if url:
        user.picture = url
        user.save()