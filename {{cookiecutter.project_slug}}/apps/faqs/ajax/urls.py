from django.urls import path, include
from .views import (
	FaqItemListAjaxView,
)

app_name = "faqs_ajax"

urlpatterns = [
    # add
    path(
        "list/",
        FaqItemListAjaxView.as_view(),
        name="list"
    ),
]
