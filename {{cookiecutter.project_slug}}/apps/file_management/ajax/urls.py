from django.urls import path, include
from .views import (
	DocumentMetadataListAjaxView,
	DocumentSubmissionListAjaxView,
)

app_name = "file_management_ajax"

urlpatterns = [
    # add
    path(
        "documents/",
        DocumentMetadataListAjaxView.as_view(),
        name="documents"
    ),
    path(
        "submissions/",
        DocumentSubmissionListAjaxView.as_view(),
        name="submissions"
    ),
]
