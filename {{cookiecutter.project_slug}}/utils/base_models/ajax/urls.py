from django.urls import path, include
from .views import (
	VerificationListAjaxView,
)

app_name = "verification_ajax"

urlpatterns = [
    # add
    path(
        "list/",
        VerificationListAjaxView.as_view(),
        name="list"
    ),
]
