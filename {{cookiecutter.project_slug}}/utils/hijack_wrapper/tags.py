from django import template
from django.contrib.auth import get_user_model

register = template.Library()

@register.inclusion_tag("list.html", takes_context=True)
def render_hijacks(context, filter=None):
    users = get_user_model().objects.all()
    if filter:
        users = users.filter(**filter)    
    context['users'] = users
    return context
