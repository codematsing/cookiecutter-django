from django.urls import path
from .views import (
	PostListAjaxView,
)

app_name = "posts_ajax"

urlpatterns = [
    # add
    path(
        "list/",
        PostListAjaxView.as_view(),
        name="list"
    ),
]
