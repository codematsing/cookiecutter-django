from django.views.generic import RedirectView
from django.urls import reverse

class NotificationUpdateAllAsRead(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        self.request.user.notifications.all().mark_all_as_read()
        return reverse("notifications_read_all")