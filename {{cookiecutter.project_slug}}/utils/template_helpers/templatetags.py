from django import template
from django.contrib.auth import get_user_model
from utils.lambdas import get_current_domain

register = template.Library()

@register.simple_tag
def current_domain():
    return get_current_domain()