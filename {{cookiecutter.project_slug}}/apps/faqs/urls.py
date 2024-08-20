from django.urls import path, include
from .views import (
ManagedFaqListView,
ManagedFaqItemCreateView,
ManagedFaqItemDetailView,
ManagedFaqItemUpdateView,
ManagedFaqItemDeleteView,
)

app_name = "faqs"

urlpatterns = [
    path(
        "",
        ManagedFaqListView.as_view(),
        name="list"
    ),
    path(
        "new/",
        ManagedFaqItemCreateView.as_view(),
        name="create"
    ),
    path(
        "<int:pk>/",
        ManagedFaqItemUpdateView.as_view(),
        name="detail"
    ),
    path(
        "<int:pk>/edit/",
        ManagedFaqItemUpdateView.as_view(),
        name="update"
    ),
    path(
        "<int:pk>/delete/",
        ManagedFaqItemDeleteView.as_view(),
        name="delete"
    ),
    path(
        "ajax/",
        include("faqs.ajax.urls",
        namespace="ajax")
    ),
]