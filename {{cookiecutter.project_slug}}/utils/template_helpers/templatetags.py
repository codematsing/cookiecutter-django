from django import template
from utils.lambdas import get_current_domain
from django.urls import reverse_lazy

register = template.Library()

@register.simple_tag
def current_domain():
    return get_current_domain()@register.simple_tag

@register.simple_tag
def full_url(url, **kwargs):
    return f"{get_current_domain()}{reverse_lazy(url, kwargs=kwargs)}"