from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .models import Registration

from utils.base_views.admin_views import (
    AdminListView,
    AdminDetailView,
    AdminUpdateView,
    AdminDeleteView
)
from utils.base_views.public_views import (
    PublicCreateView,
)


import logging
logger = logging.getLogger(__name__)

# Create your views here.
class RegistrationListView(SuccessMessageMixin, AdminListView):
    model = Registration
    template_name='registrations/list.html'

class RegistrationCreateView(SuccessMessageMixin, PublicCreateView):
    model = Registration
    success_message = _("Registration request created. Please check your email for updates")
    hidden_fields = ['is_approved']
    disabled_fields = ['is_approved']
    template_name='registrations/create.html'

    def get_success_url(self):
        return reverse(
            "user_registration:list",
        )

class RegistrationDetailView(SuccessMessageMixin, AdminDetailView):
    model = Registration

class RegistrationUpdateView(SuccessMessageMixin, AdminUpdateView):
    model = Registration

class RegistrationDeleteView(SuccessMessageMixin, AdminDeleteView):
    model = Registration

class RegistrationApproveView(SuccessMessageMixin, AdminDeleteView):
    model = Registration
    template_name='registrations/approve.html'
    success_message = _("User has been approved.")

    def form_valid(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_approved = True
        self.object.save()
        return redirect(self.get_success_url())

class RegistrationRejectView(SuccessMessageMixin, AdminDeleteView):
    model = Registration
    template_name='registrations/reject.html'
    success_message = _("User has been rejected.")