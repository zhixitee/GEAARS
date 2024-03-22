from django.contrib import admin
from .models import Category, Event, UserEvent, UserProfile, CommentReview, EventReview,Feedback

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'organizer', 'slug')
    prepopulated_fields = {'slug': ('title',)}  

class UserEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'timestamp')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'picture')

class CommentReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'content')

class EventReviewAdmin(admin.ModelAdmin):
    list_display = ('review_ID', 'user', 'event', 'atmosphere_rating', 'concession_price_rating', 'artist_rating', 'value_rating', 'location_rating' )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(UserEvent, UserEventAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CommentReview, CommentReviewAdmin)
admin.site.register(EventReview, EventReviewAdmin)
admin.site.register(Feedback)