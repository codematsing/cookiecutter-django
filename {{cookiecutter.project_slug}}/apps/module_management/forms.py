from utils.base_forms.forms import BaseModelForm
from django import forms
from formset.widgets import Selectize, DualSelector
from module_management.models import SidebarItem
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
        self.fields['href'].widget.choices = ((url, url) for url in get_url_df(as_url_list=True))

    class Meta:
        model = SidebarItem
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
