from django.urls import path, include
from .views import (
	ModuleManagementListAjaxView,
    SidebarAjaxView
)

app_name = "module_management_ajax"

urlpatterns = [
    # add
    path(
        "list/",
        ModuleManagementListAjaxView.as_view(),
        name="list"
    ),
    path(
        "sidebar/",
        SidebarAjaxView.as_view(),
        name="sidebar"
    ),
]
