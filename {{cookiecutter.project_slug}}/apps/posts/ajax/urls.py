from django.urls import path, include
from .views import (
	PostListAjaxView,
    ScholarshipPostListAjaxView,
    BlogPostListAjaxView,
)

app_name = "posts_ajax"

urlpatterns = [
    # add
    path(
        "list/",
        PostListAjaxView.as_view(),
        name="list"
    ),
    path(
        "blogs/",
        BlogPostListAjaxView.as_view(),
        name="blogs_list"
    ),
    path(
        "scholarships/",
        ScholarshipPostListAjaxView.as_view(),
        name="scholarships_list"
    ),
]
