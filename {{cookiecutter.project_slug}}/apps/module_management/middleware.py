from module_management.models import NavItem, AccessClassification
from django.http import HttpResponseForbidden
from django.urls import resolve
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from utils.lambdas import get_url_df
import logging
logger = logging.getLogger(__name__)

def get_root_module_list_url(request_url):
    # get root NavItem because if you do not have access to root NavItem,
    # you should not have access to submodules

    #posts/managed_list/ special case
    _list = request_url.strip("/").split("/")
    for index in range(len(_list)):
        url = f'/{"/".join(_list[:index+1])}/'
        if NavItem.objects.filter(href=url).exists():
            return url
    return request_url

def can_url_bypass_middleware(url):
    sidebar_ajax_url = reverse("modules:ajax:sidebar")
    home_url = reverse("home")
    history_ajax_url = reverse("history:list")

    bypass_urls = [home_url, sidebar_ajax_url, history_ajax_url]
    check_module_apps = settings.LOCAL_APPS + []
    df = get_url_df()
    return (
        (url in bypass_urls) 
        or (df.query(f"url=='{url}' and module_app in {check_module_apps}").empty)
        or "inbox/notifications/" in url
        )

def module_management_middleware(get_response):
    """First layer permission that allows access based on visibility of sidebar item
    for a particular user.
    """
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        user = request.user
        root_url = get_root_module_list_url(request.path)
        nav_items = NavItem.objects.filter(href__in={request.path, root_url})
        response = get_response(request)

        if can_url_bypass_middleware(request.path):
            return response

        for sidebar_item in nav_items:
            if (
                (sidebar_item.classification == AccessClassification.INTERNAL and user.is_authenticated) 
                or (sidebar_item.classification==AccessClassification.CONFIDENTIAL and user.groups.filter(nav_items=sidebar_item).exists())
                or (sidebar_item.classification==AccessClassification.PUBLIC)
                or (user.is_superuser or user.is_staff)
                ):
                    return response

        logger.warning(f"Custom Middleware will force Http Response Forbidden for {request.path}")
        messages.error(request, "Sorry, the url you are trying to access is not found.")
        if user.is_authenticated:
            return redirect("dashboard")
        return redirect("home")


    return middleware