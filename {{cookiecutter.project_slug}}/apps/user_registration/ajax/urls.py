from django.urls import path, include
from .views import (
	RegistrationListAjaxView,
)

app_name = "user_registration_ajax"

urlpatterns = [
    path(
        "list/",
        RegistrationListAjaxView.as_view(),
        name="list"
    ),
]
