from django import template

register = template.Library()


@register.inclusion_tag("detail.html", takes_context=True)
def render_detail(context, update_permission=None, delete_permission=None):
    _object = context['object']
    _request = context['request']
    update_permission = update_permission if update_permission else f"{_object._meta.app_label}.change_{_object._meta.model_name}"
    delete_permission = delete_permission if delete_permission else f"{_object._meta.app_label}.delete_{_object._meta.model_name}"
    context['has_change_permission'] = _request.user.has_perm(update_permission, _object)
    context['has_delete_permission'] = _request.user.has_perm(delete_permission, _object)
    return context