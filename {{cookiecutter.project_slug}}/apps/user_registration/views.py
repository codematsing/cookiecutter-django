from urllib.parse import urlencode
from base64 import b64decode

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django import forms

from utils.permissions import IsSAOPermissionMixin, IsStudentOwnerPermissionMixin

from formset.widgets import DateInput

from .models import Registration

from allauth.account.views import SignupView

from utils.base_views.views import (

    BaseDeleteView,
    BaseActionView,
    BaseAddObjectView,
    BaseRemoveObjectView,
    BaseActionObjectView,
)

from utils.base_views.admin_views import (
    AdminListView,
    AdminCreateView,
    AdminDetailView,
    AdminUpdateView,
    AdminDeleteView
)

from utils.base_views.public_views import (
    PublicCreateView,
)


import logging
logger = logging.getLogger(__name__)

class ApprovedSignupView(SignupView):
    def get_form(self, *args, **kwargs):
        form = super(ApprovedSignupView, self).get_form(*args, **kwargs)
        if 'signup_code' in self.kwargs:
            signup_info = b64decode(self.kwargs['signup_code']).decode().split("_")
            form.fields['username'].initial = signup_info[1]
            form.fields['email'].initial = signup_info[2]
        form.fields['username'].widget.attrs['readonly'] = True
        form.fields['email'].widget.attrs['readonly'] = True
        return form

# Create your views here.
class RegistrationListView(IsSAOPermissionMixin, SuccessMessageMixin, AdminListView):
    model = Registration
    template_name='registrations/list.html'

    def get_header_buttons(self):
        return {}

class RegistrationCreateView(PublicCreateView):
    model = Registration
    success_message = _("Registration request created. Please check your email for updates")
    hidden_fields = ['is_approved']
    disabled_fields = ['is_approved']
    template_name='registrations/create.html'

    def get_form(self):
        form = super(RegistrationCreateView, self).get_form()
        form.fields['birth_date'] = forms.DateField(required=True, widget=DateInput())
        return form

    def get_success_url(self):
        return reverse(
            "user_registration:list",
        )

class RegistrationDetailView(IsSAOPermissionMixin, AdminDetailView):
    model = Registration

class RegistrationUpdateView(IsSAOPermissionMixin, AdminUpdateView):
    model = Registration

class RegistrationDeleteView(IsSAOPermissionMixin, AdminDeleteView):
    model = Registration

class RegistrationApproveView(IsSAOPermissionMixin, AdminUpdateView):
    model = Registration
    template_name='registrations/approve.html'
    fields = ["is_approved"]
    disabled_fields = ["is_approved"]

    def get_form_header(self):
        return "Registration Status"

    def get_initial(self):
        return {"is_approved":True}

    def get_success_message(self, cleaned_data):
        return f"{self.get_object()} has been approved user_account"

    def get_success_url(self):
        return reverse("user_registration:list")

class RegistrationRejectView(RegistrationApproveView):
    def get_initial(self):
        return {"is_approved":False}

    def get_success_message(self, cleaned_data):
        return f"{self.get_object()} has been denied user account"
