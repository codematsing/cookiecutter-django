from utils.base_forms.forms import BaseModelForm
from django import forms
from formset.widgets import Selectize, DualSelector
from module_management.models import NavItem
from django.conf import settings
from django.contrib.auth.models import Group
from django.urls import resolve
import logging
logger = logging.getLogger(__name__)

class ModuleModelForm(BaseModelForm):
    groups = forms.ModelMultipleChoiceField(required=False, queryset=Group.objects.all(), widget=DualSelector(attrs={'df-show':".classification==2"}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # initializing choices on runtime due to circular import
        from utils.lambdas import get_url_df
        third_party_apps_to_exclude = list(set(settings.THIRD_PARTY_APPS).difference({"notifications",}))
        exclude_modules = ["file_management", "django", "debug_toolbar", "hijack"] + settings.DJANGO_APPS + third_party_apps_to_exclude
        exclude_notifications_except_all = "(~name.str.contains('notifications') or name.str.contains('notifications:all'))"
        exclude_urls_with_params = "~url.str.contains('<|>')"
        exclude_ajax = "~url.str.contains('ajax')"
        exclude_create_or_update = "~name.str.contains('create|update')"
        filter_query = " and ".join([exclude_notifications_except_all, exclude_urls_with_params, exclude_ajax, exclude_create_or_update])

        self.fields['href'].widget.choices = ((url, url) for url in get_url_df(return_type=list, exclude_modules=exclude_modules, filter_query=filter_query))

    class Meta:
        model = NavItem
        fields = '__all__'
        widgets = {
            'href':Selectize()
        }

    def save(self, commit=True):
        instance = super().save()
        groups = self.cleaned_data['groups']
        instance.groups.clear()
        instance.groups.add(*groups)
        return instance
