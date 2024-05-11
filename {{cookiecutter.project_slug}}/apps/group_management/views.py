from django.shortcuts import render
from django.contrib.auth.models import Group
from group_management.forms import GroupForm

from utils.base_views.admin_views import (
	AdminListView,
	AdminCreateView,
	AdminDetailView,
	AdminUpdateView,
	AdminDeleteView
)

from django.urls import reverse


import logging
logger = logging.getLogger(__name__)

# Create your views here.
class GroupManagementListView(AdminListView):
	model = Group

	def get_ajax_list_url(self):
		return reverse("group_management:ajax:list")

	def get_header_buttons(self):
		return [{'label':'Add', 'href':reverse("group_management:create")}]

class GroupManagementCreateView(AdminCreateView):
	model = Group
	form_class = GroupForm

	def get_success_url(self):
		return reverse("group_management:list")

class GroupManagementUpdateView(AdminUpdateView):
	model = Group
	form_class = GroupForm

	def get_initial(self):
		initial = super().get_initial()
		initial['modules'] = self.get_object().sidebar_items.all()
		initial['users'] = self.get_object().user_set.all()
		initial['custom_permissions'] = self.get_object().permissions.exists()
		return initial

	def get_success_url(self):
		return reverse("group_management:list")