from django.urls import path, include

from users.user_management_views import (
    ManagedUserSearchForm,
    ManagedUserDetailView,
    ManagedUserUpdateView,
)

app_name = "user_management"
urlpatterns = [
    path("", view=ManagedUserSearchForm.as_view(), name="search"),
    path("<str:username>/", view=ManagedUserDetailView.as_view(), name="detail"),
    path("<str:username>/edit/", view=ManagedUserUpdateView.as_view(), name="update"),
]
