from django.urls import path

from users.views import (
    UserProfileDetailView,
    UserProfileUpdateView,
)

app_name = "profile"

urlpatterns = [
    path("", view=UserProfileDetailView.as_view(), name="detail"),
    path("edit/", view=UserProfileUpdateView.as_view(), name="update"),
]
