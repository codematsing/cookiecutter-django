from django import template
from django.urls import resolve
from django.template.defaultfilters import stringfilter
import markdown as md

register = template.Library()


@register.inclusion_tag("form.html", takes_context=True)
def render_detail(context, object_update_url=None):
    if object_update_url:
        context["object_update_url"] = object_update_url
    return context
