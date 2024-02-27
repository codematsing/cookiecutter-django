from django import template
from utils.lambdas import get_current_domain

register = template.Library()

@register.simple_tag
def current_domain():
    return get_current_domain()