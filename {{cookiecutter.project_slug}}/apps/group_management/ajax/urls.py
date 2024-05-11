from django.urls import path, include
from .views import (
	GroupManagementListAjaxView,
)

app_name = "group_management_ajax"

urlpatterns = [
    # add
    path(
        "list/",
        GroupManagementListAjaxView.as_view(),
        name="list"
    ),
]
