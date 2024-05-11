from utils.base_forms.forms import CustomDualSelector, BaseModelForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from module_management.models import SidebarItem
from django import forms
    
class GroupForm(BaseModelForm):
    users = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.exclude(username="AnonymousUser"), widget=CustomDualSelector(), required=False)
    modules = forms.ModelMultipleChoiceField(queryset=SidebarItem.objects.all(), widget=CustomDualSelector(), required=False)
    custom_permissions = forms.BooleanField(label="Customize Model Permissions", initial=True)
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), widget=CustomDualSelector(attrs={'df-hide':".custom_permissions==''"}), required=False)

    field_order = ['name', 'users', 'modules', 'custom_permissions', 'permissions']
    class Meta:
        model = Group
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit)
        users = self.cleaned_data["users"]
        instance.user_set.add(*users)
        sidebar_items = self.cleaned_data["modules"]
        instance.sidebar_items.add(*sidebar_items)
        permissions = self.cleaned_data["permissions"]
        instance.permissions.add(*permissions)
        return instance