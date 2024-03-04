from django.contrib import admin
from events.models import Category, Page
from events.models import UserProfile
# Register your models here.


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slugs': ('name',)}


admin.site.register(Category)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
