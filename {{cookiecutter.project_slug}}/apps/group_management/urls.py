from django.urls import path, include
from .views import (
GroupManagementListView,
GroupManagementCreateView,
GroupManagementUpdateView,
)

app_name = "group_management"

# Make sure you add urls to model.spy
# add get_<name>_url() method

urlpatterns = [
    # list
    path(
        "",
        GroupManagementListView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        GroupManagementCreateView.as_view(),
        name="create"
    ),
    # update
    path(
        "<int:pk>/edit/",
        GroupManagementUpdateView.as_view(),
        name="update"
    ),
    path(
        "ajax/",
        include("group_management.ajax.urls",
        namespace="ajax")
    ),
]