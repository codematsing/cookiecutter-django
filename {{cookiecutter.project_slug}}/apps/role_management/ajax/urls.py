from django.urls import path
from .views import (
	RoleListAjaxView,
    RoleUsersListAjaxView,
    RoleModulesListAjaxView
)

app_name = "role_management_ajax"

urlpatterns = [
    # add
    path(
        "list/",
        RoleListAjaxView.as_view(),
        name="list"
    ),
    path(
        "users/",
        RoleUsersListAjaxView.as_view(),
        name="users_list"
    ),
    path(
        "modules/",
        RoleModulesListAjaxView.as_view(),
        name="modules_list"
    ),
]
