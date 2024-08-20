from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from utils.base_views.admin_views import AdminDetailView, AdminUpdateView
from users.forms import UserProfileForm

User = get_user_model()

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

user_detail_view = UserDetailView.as_view()

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user

user_update_view = UserUpdateView.as_view()

class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

user_redirect_view = UserRedirectView.as_view()

class UserProfileDetailView(AdminDetailView):
    model = User
    template_name="pages/admin/profile/detail.html"
    show_history = False

    def get_header_buttons(self):
        update_url = self.request.user.get_profile_update_url()
        return [
            {'label':'Edit', 'icon':'mdi-pencil', 'href': update_url},
        ]

    def get_object(self):
        return self.request.user

class UserProfileUpdateView(AdminUpdateView):
    model = User
    form_class = UserProfileForm
    form_header = "Profile Update Form"
    breadcrumb_name = "Profile"

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse("profile:detail")