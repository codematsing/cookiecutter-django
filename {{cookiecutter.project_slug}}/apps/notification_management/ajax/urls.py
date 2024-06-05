from django.urls import path, include
from .views import (
	NotificationsListAjaxView,
	NotificationUpdateUnreadAjaxView
)

app_name = "notification_management_ajax"

urlpatterns = [
    path("list/", NotificationsListAjaxView.as_view(), name="list" ),
    path("update/", NotificationUpdateUnreadAjaxView.as_view(), name="update_status" ),
]
