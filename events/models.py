from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, related_name='organized_events', on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(null=False, unique=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d')}"

class UserEvent(models.Model):
    STATUS_CHOICES = [('attending', 'Attending'), ('interested', 'Interested'), ('declined', 'Declined')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='interested')
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"


    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class CommentReview(models.Model):
    comment_ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    content = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comment_reviews", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class EventReview(models.Model):
    review_ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    user = models.ForeignKey(User, related_name="event_review", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    atmosphere_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    concession_price_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    artist_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    value_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    location_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.user.username

