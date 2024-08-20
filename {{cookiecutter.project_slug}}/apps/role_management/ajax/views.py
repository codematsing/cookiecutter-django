from django.shortcuts import render, get_object_or_404
from role_management.models import Role
from module_management.models import NavItem
from django.contrib.auth import get_user_model
from utils.base_views.ajax.views import (
	BaseListAjaxView,
)
from django.template.loader import render_to_string

# Create your views here.

class RoleListAjaxView(BaseListAjaxView):
	model = Role

	def customize_row(self, row, obj):
		row['action'] = render_to_string('role_management/action_column.html', {'record':obj, 'has_update_permission':self.get_update_permission()}) 
		return

class RoleUsersListAjaxView(BaseListAjaxView):
	model = get_user_model()
	def get_column_defs(self, request):
		return [
			{"name":"pk", "visible":False},
			{"name":"username", "searchable":True},
			{"name":"employee_number", "searchable":True},
		]
	initial_order = [["username", "asc"]]

	def get_initial_queryset(self, request):
		pk = self.request.REQUEST.get('pk', None)
		obj = get_object_or_404(Role, pk=pk)
		return obj.user_set.all()

class RoleModulesListAjaxView(BaseListAjaxView):
	model = NavItem
	def get_column_defs(self, request):
		return [
			{"name":"pk", "visible":False},
			{"name":"header", "searchable":True},
			{"name":"label", "searchable":True},
			{"name":"href", "searchable":True},
		]
	initial_order = [["header", "asc"]]

	def get_initial_queryset(self, request):
		pk = self.request.REQUEST.get('pk', None)
		obj = get_object_or_404(Role, pk=pk)
		return obj.nav_items.all()