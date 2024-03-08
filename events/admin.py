from django.contrib import admin
from events.models import Category, Page, Event, UserEvent
from events.models import UserProfile
# Register your models here.

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slugs': ('name',)}


admin.site.register(Category)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(UserEvent)
