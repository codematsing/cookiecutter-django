from django.urls import path, include
from notification_management.views import NotificationUpdateAllAsRead
from notifications.urls import urlpatterns

app_name = "notification_management"

urlpatterns += [
    path("mark-all-as-read/", NotificationUpdateAllAsRead.as_view(), name="read_all" ),
    path(
        "ajax/",
        include("notification_management.ajax.urls",
        namespace="ajax")
    ),
]