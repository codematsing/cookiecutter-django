from django.shortcuts import render
from utils.base_views.ajax.views import (
	BaseListAjaxView,
)
from django.contrib.auth.models import Group
from django.template.loader import render_to_string

# Create your views here.

class GroupManagementListAjaxView(BaseListAjaxView):
	model = Group

	def customize_row(self, row, obj):
		row['action'] = render_to_string('group_management/action_column.html', {'record':obj, 'has_update_permission':self.get_update_permission()}) 
		return