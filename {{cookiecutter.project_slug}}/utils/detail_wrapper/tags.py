from django import template
from django.urls import resolve
from django.template.defaultfilters import stringfilter
import markdown as md

register = template.Library()


@register.inclusion_tag("detail.html", takes_context=True)
def render_detail(context, update_object_link=None):
    if update_object_link:
        context["update_object_link"] = update_object_link
    return context
