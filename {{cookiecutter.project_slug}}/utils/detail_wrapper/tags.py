from django import template

register = template.Library()


@register.inclusion_tag("detail_wrapper/detail.html", takes_context=True)
def render_detail(context):
    _object = context['object']
    _request = context['request']
    return context