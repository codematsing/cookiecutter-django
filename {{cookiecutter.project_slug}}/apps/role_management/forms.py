from utils.base_forms.forms import CustomDualSelector, BaseModelForm
from role_management.models import Role
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from module_management.models import NavItem, AccessClassification
from django import forms


class RoleForm(BaseModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.exclude(username="AnonymousUser"),
        widget=CustomDualSelector(),
        required=False,
    )
    modules = forms.ModelMultipleChoiceField(
        queryset=NavItem.objects.exclude(
            classification__in=[
                AccessClassification.INTERNAL,
                AccessClassification.PUBLIC,
            ]
        ),
        help_text="Public and Internal modules have been filtered out",
        widget=CustomDualSelector(),
        required=False,
    )
    custom_permissions = forms.BooleanField(
        label="Customize Model Permissions", 
        help_text="Please coordinate with developers regarding this section", 
        initial=False, 
        required=False
    )
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=CustomDualSelector(attrs={"df-hide": ".custom_permissions==''"}),
        required=False,
    )

    field_order = ["name", "users", "modules", "custom_permissions", "permissions"]

    class Meta:
        model = Role
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit)
        users = self.cleaned_data["users"]
        instance.user_set.add(*users)
        nav_items = self.cleaned_data["modules"]
        instance.nav_items.add(*nav_items)
        permissions = self.cleaned_data["permissions"]
        instance.permissions.add(*permissions)
        return instance
