from django.shortcuts import render
from .models import SidebarItem
from utils.base_views.admin_views import (
	AdminListView,
	AdminCreateView,
	AdminDetailView,
	AdminUpdateView,
	AdminDeleteView
)
from django.urls import reverse
from module_management.forms import ModuleModelForm


import logging
logger = logging.getLogger(__name__)

# Create your views here.
class ModuleManagementListView(AdminListView):
	model = SidebarItem
	def get_ajax_list_url(self):
		return reverse("modules:ajax:list")

class ModuleManagementCreateView(AdminCreateView):
	model = SidebarItem
	form_class = ModuleModelForm

class ModuleManagementDetailView(AdminDetailView):
	model = SidebarItem

class ModuleManagementUpdateView(AdminUpdateView):
	model = SidebarItem
	form_class = ModuleModelForm

class ModuleManagementDeleteView(AdminDeleteView):
	model = SidebarItem
