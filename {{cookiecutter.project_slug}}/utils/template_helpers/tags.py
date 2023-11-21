# How to create custom template tags and filters
from django import template
from django.contrib.auth import get_user_model
from django.conf import settings

register = template.Library()


@register.simple_tag
def active_namespace(request, namespace):
    """Returns "active" if namespace evaluation is True.
    Use use for navlink highlighting

    Args:
        request (request): pass request
        namespace (string): pass namespace evaluation

    Returns:
        _type_: _description_
    """
    app_names = request.resolver_match.app_names
    app_names.append(request.resolver_match.url_name)
    res_path = ":".join(app_names)
    if namespace in res_path:
        return "active"
    return ""


# @register.inclusion_tag("/path/to/template", takes_context=True)
# def func(context, *args):
#    return context

@register.simple_tag
def get_all_users():
    return get_user_model().objects.filter()

@register.simple_tag
def get_settings_value(name):
    """Returns a value from settings.py

    Args:
        name (_type_): str

    Returns:
        value
    """
    return getattr(settings, name, None)