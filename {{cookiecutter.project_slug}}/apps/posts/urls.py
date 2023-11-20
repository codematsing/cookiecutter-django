from django.urls import path, include
from .views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
)

app_name = "posts"

urlpatterns = [
    # list
    path(
        "",
        PostListView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        PostCreateView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        PostDetailView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        PostUpdateView.as_view(),
        name="update"
    ),
    # delete
    path(
        "<int:pk>/delete/",
        PostDeleteView.as_view(),
        name="delete"
    ),
    # apply
    path(
        "ajax/",
        include("posts.ajax.urls",
        namespace="ajax")
    ),
]
