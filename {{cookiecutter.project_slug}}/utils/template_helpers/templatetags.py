from django import template
from utils.lambdas import get_current_domain
from django.urls import reverse_lazy
from django.middleware.csrf import get_token
from django import template
from django.middleware.csrf import get_token
from formset.templatetags.formsetify import _formsetify

import logging
logger = logging.getLogger(__name__)

register = template.Library()

@register.simple_tag
def current_domain():
    return get_current_domain()

@register.simple_tag
def full_url(url, **kwargs):
    return f"{get_current_domain()}{reverse_lazy(url, kwargs=kwargs)}"

def render_form(context, form, *args, **kwargs):
    get_token(context['request'])  # ensures that the CSRF-Cookie is set
    form = _formsetify(form, *args, **kwargs)
    return form.render()

register.simple_tag(render_form, name='render_form', takes_context=True)