from django.urls import path, include
from .views import (
    ManagedPostListView,
    ManagedPostCreateView,
    ManagedPostUpdateView,
    ManagedPostDeleteView,
)

app_name = "posts"

urlpatterns = [
    path(
        "",
        ManagedPostListView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        ManagedPostCreateView.as_view(),
        name="create"
    ),
    # update
    path(
        "<int:pk>/edit/",
        ManagedPostUpdateView.as_view(),
        name="update"
    ),
    # delete
    path(
        "<int:pk>/delete/",
        ManagedPostDeleteView.as_view(),
        name="delete"
    ),
    # apply
    path(
        "ajax/",
        include("posts.ajax.urls",
        namespace="ajax")
    ),
]
