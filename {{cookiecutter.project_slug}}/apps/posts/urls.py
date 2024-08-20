from django.urls import path, include
from .views import (
    PostListView,
    ScholarshipApplicationRedirectView,
    ScholarshipPostListView,
    BlogPostListView,
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
    path(
        "scholarships/",
        ScholarshipPostListView.as_view(),
        name="scholarship_list"
    ),
    path(
        "blogs/",
        BlogPostListView.as_view(),
        name="blog_list"
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
        "<int:pk>/apply/",
        ScholarshipApplicationRedirectView.as_view(),
        name="apply_redirect"
    ),
    path(
        "ajax/",
        include("posts.ajax.urls",
        namespace="ajax")
    ),
]
