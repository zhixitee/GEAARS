from django import template
from events.models import Category

register = template.Library()

@register.inclusion_tag('events/categories.html')
def get_category_list():
    return {'categories': Category.objects.all()}