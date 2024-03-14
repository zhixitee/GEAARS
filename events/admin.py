from django.contrib import admin
from .models import Category, Event, UserEvent, UserProfile

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'organizer', 'slug')
    prepopulated_fields = {'slug': ('title',)}  

class UserEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'timestamp')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'picture')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(UserEvent, UserEventAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
