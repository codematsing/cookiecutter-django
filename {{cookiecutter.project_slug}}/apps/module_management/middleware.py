from module_management.models import SidebarItem, SidebarClassification
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
    # get root SidebarItem because if you do not have access to root SidebarItem,
    # you should not have access to submodules
    _list = request_url.strip("/").split("/")
    for index in range(len(_list)):
        url = f'/{"/".join(_list[:index+1])}/'
        if SidebarItem.objects.filter(href=url).exists():
            return url
    return request_url

def can_url_bypass_middleware(url):
    bypass_urls = ["/", "/modules/ajax/sidebar"]
    check_module_apps = settings.LOCAL_APPS + []
    df = get_url_df()
    return url in bypass_urls or df.query(f"url=='{url}' and module_app in {check_module_apps}").empty 

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
        sidebar_items = SidebarItem.objects.filter(href__in={request.path, root_url})
        response = get_response(request)

        if user.is_superuser or user.is_staff or can_url_bypass_middleware(request.path):
            return response

        for sidebar_item in sidebar_items:
            if (
                (sidebar_item.classification == SidebarClassification.INTERNAl and user.is_authenticated) 
                or (sidebar_item.classification==SidebarClassification.CONFIDENTIAL and user.groups.filter(sidebar_items=sidebar_item).exists())
                or (user.is_superuser or user.is_staff)
                ):
                    return response

        logger.warning(f"Custom Middleware will force Http Response Forbidden for {request.path}")
        messages.error(request, "Sorry, the url you are trying to access is not found.")
        if user.is_authenticated:
            return redirect("dashboard")
        return redirect("home")


    return middleware