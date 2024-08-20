from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView
from utils.base_views.views import BaseFormMixin
from utils.base_views.admin_views import AdminDetailView, AdminUpdateFormCollectionView
from users.forms import UserSearchForm, UserUpdateFormCollectionForm
from django.http import JsonResponse
from django.shortcuts import redirect
from users.views import UserProfileDetailView
from django.urls import reverse_lazy
import logging

logger = logging.getLogger(__name__)


class ManagedUserSearchForm(BaseFormMixin, FormView):
    form_class = UserSearchForm
    template_name = "pages/admin/form.html"

    def get_success_url(self):
        # remove initial success_url wait until form_valid to load success_url
        return None

    def form_valid(self, form):
        _user = form.get_user()
        success_url = reverse_lazy(
                    "user_management:detail", kwargs={"username": _user.username}
                )
        return JsonResponse(
            {
                "success_url": success_url,
                "next_page_url": success_url
            }
        )

    def get_form_header(self):
        return "Search User"

class ManagedUserDetailView(UserProfileDetailView):
    show_history = True
    model = get_user_model()
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_object(self):
        return self.model.objects.get(username=self.kwargs['username'])

    def get_header_buttons(self):
        return [
            {"label":"Update Profile", "href":reverse_lazy("user_management:update", kwargs={"username":self.kwargs["username"]})}
        ]

class ManagedUserUpdateView(AdminUpdateFormCollectionView):
    model = get_user_model()
    slug_field = "username"
    slug_url_kwarg = "username"
    collection_class = UserUpdateFormCollectionForm

    def get_initial(self):
        _object = self.get_object()
        return {
            "user_profile": {
                field.name: getattr(_object, field.name, None) for field in _object._meta.fields
            },
            "unit_role_formset": [
                {'unit_role_form': {
                    "unit":unit_role.unit,
                    "role":unit_role.role,
                    "is_primary":unit_role==_object.primary_unit_role
                }} for unit_role in _object.unit_roles.all()
            ]
        }