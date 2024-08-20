from django.shortcuts import render
from .models import Role
from role_management.forms import RoleForm
from django.urls import reverse

from utils.base_views.admin_views import (
	AdminListView,
	AdminCreateView,
	AdminDetailView,
	AdminUpdateView,
	AdminDeleteView
)


import logging
logger = logging.getLogger(__name__)

# Create your views here.
class RoleListView(AdminListView):
	model = Role

class RoleCreateView(AdminCreateView):
	model = Role
	form_class = RoleForm

class RoleDetailView(AdminDetailView):
	model = Role
	template_name = "role_management/detail.html"

class RoleUpdateView(AdminUpdateView):
	model = Role
	form_class = RoleForm

	def get_initial(self):
		initial = super().get_initial()
		initial['modules'] = self.get_object().nav_items.all()
		initial['users'] = self.get_object().user_set.all()
		initial['custom_permissions'] = self.get_object().permissions.exists()
		return initial

	def get_success_url(self):
		return reverse("role_management:list")

class RoleDeleteView(AdminDeleteView):
	model = Role

# class Role<snake_case_action>View(BaseActionView):
# 	model= Role

# class RoleAdd<model_name_camel_case_fk>View(BaseAddObjectView):
# 	model= Role

# class RoleRemove<model_name_camel_case_fk>View(BaseRemoveObjectView):
# 	model= Role

# class Role<snake_case_action><model_name_camel_case_fk>View(BaseActionObjectView):
# 	model= Role