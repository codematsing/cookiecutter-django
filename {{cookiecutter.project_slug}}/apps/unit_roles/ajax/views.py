from django.shortcuts import render
from unit_roles.models import UnitRole
from utils.base_views.ajax.views import (
	BaseListAjaxView,
	BaseCreateAjaxView,
	BaseDetailAjaxView,
	BaseUpdateAjaxView,
	BaseDeleteAjaxView,
	BaseActionAjaxView,
	BaseAddObjectAjaxView,
	BaseRemoveObjectAjaxView,
	BaseActionObjectAjaxView,
)

# Create your views here.

class UnitRoleListAjaxView(BaseListAjaxView):
	model = UnitRole

class UnitRoleCreateAjaxView(BaseCreateAjaxView):
	model = UnitRole

class UnitRoleDetailAjaxView(BaseDetailAjaxView):
	model = UnitRole

class UnitRoleUpdateAjaxView(BaseUpdateAjaxView):
	model = UnitRole

class UnitRoleDeleteAjaxView(BaseDeleteAjaxView):
	model = UnitRole

# class UnitRole<snake_case_action>AjaxView(BaseActionAjaxView):
# 	model = UnitRole

# class UnitRoleAdd<model_name_camel_case_fk>AjaxView(BaseAddObjectAjaxView):
# 	model = UnitRole

# class UnitRoleRemove<model_name_camel_case_fk>AjaxView(BaseRemoveObjectAjaxView):
# 	model = UnitRole

# class UnitRole<snake_case_action><model_name_camel_case_fk>AjaxView(BaseActionObjectAjaxView):
# 	model = UnitRole