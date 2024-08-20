from module_management.models import NavItem, AccessClassification
from django.http import HttpResponseForbidden
from django.urls import resolve
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from utils.lambdas import get_url_df

from module_management.middleware import can_url_bypass_middleware

import logging
logger = logging.getLogger(__name__)

def user_profile_middleware(get_response):
    """First layer permission that allows access based on visibility of sidebar item
    for a particular user.
    """
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        user = request.user
        response = get_response(request)

        if can_url_bypass_middleware(request.path):
            return response

        profile_edit_url = user.get_profile_update_url()
        if profile_edit_url == request.path:
            return response

        if any(getattr(user, field, None) is None for field in user.get_profile_required_fields):
            logger.warning(f"Custom Middleware will force redirect {request.path} to user profile")
            messages.error(request, "It seems that you do not have your profile set. You are required to update this before you can access the QAO portal")
            return redirect(profile_edit_url)

        if user.is_authenticated:
            return response
        return redirect("home")

    return middleware