from django import forms
from unit_roles.forms import UnitRoleFormset
from utils.base_forms.forms import BaseFormCollection, BaseModelForm, BaseForm, LogEntryForm
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from unit_roles.models import UnitRole
import logging
logger = logging.getLogger(__name__)
User = get_user_model()

class UserSearchForm(BaseForm):
    legend = "Search User"

    username = forms.CharField(
        label="Username", 
        help_text="Input username to manage",
        max_length=128, 
        required=False,
        )
    employee_number = forms.CharField(
        label="Employee Number", 
        help_text="Input employee number to manage",
        max_length=128, 
        required=False,
        )

    def get_user(self):
        qs = get_user_model().objects.all()
        if username := self.cleaned_data["username"]:
            qs = qs.filter(username=username)
        if employee_number := self.cleaned_data["employee_number"]:
            qs = qs.filter(employee_number=employee_number)
        if qs.exists():
            return qs.first()
        return qs.none()

    def clean(self):
        if not self.get_user():
            raise ValidationError("Cannot find employee given information provided")

class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User

class UserProfileForm(BaseModelForm):
    legend = "User Profile"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info(self.fields)
        required_fields = [
            "honorifics",
            "first_name",
            "last_name",
            "employee_number",
        ]
        for field_name, field in self.fields.items():
            if field_name in required_fields:
                field.required=True
    class Meta:
        model = get_user_model()
        fields = [
            "honorifics",
            "first_name",
            "middle_name",
            "last_name",
            "suffix",
            "employee_number",
        ]

class UserUpdateFormCollectionForm(BaseFormCollection):
    user_profile = UserProfileForm()
    unit_role_formset = UnitRoleFormset()
    log_entry_form = LogEntryForm()

    def save(self):
        instance = UserProfileForm(initial=self.cleaned_data["user_profile"], instance=self.instance).save(commit=False)
        if log_entry:=self.cleaned_data["log_entry_form"]["log_entry"]:
            instance._additional_data = {
                "Log Entry": log_entry
            }
        instance.save()
        for unit_role_form in self.cleaned_data["unit_role_formset"]:
            unit_role_kwargs = unit_role_form["unit_role_form"]
            is_primary = unit_role_kwargs.pop('is_primary', False)
            unit_role, created = UnitRole.objects.update_or_create(**unit_role_kwargs)
            if marked_for_removal := unit_role_kwargs.pop('_marked_for_removal_', False):
                instance.unit_roles.remove(unit_role)
            else:
                instance.unit_roles.add(unit_role)
                if is_primary:
                    instance.primary_unit_role = unit_role
                    instance.save()
        return instance

class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
