from django.shortcuts import render
from .models import UnitRole
from utils.base_views.views import (
	
	BaseDeleteView,
	BaseActionView,
	BaseAddObjectView,
	BaseRemoveObjectView,
	BaseActionObjectView,
)

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
class UnitRoleListView(AdminListView):
	model = UnitRole

class UnitRoleCreateView(AdminCreateView):
	model = UnitRole

class UnitRoleDetailView(AdminDetailView):
	model = UnitRole

class UnitRoleUpdateView(AdminUpdateView):
	model = UnitRole

class UnitRoleDeleteView(AdminDeleteView):
	model = UnitRole

# class UnitRole<snake_case_action>View(BaseActionView):
# 	model= UnitRole

# class UnitRoleAdd<model_name_camel_case_fk>View(BaseAddObjectView):
# 	model= UnitRole

# class UnitRoleRemove<model_name_camel_case_fk>View(BaseRemoveObjectView):
# 	model= UnitRole

# class UnitRole<snake_case_action><model_name_camel_case_fk>View(BaseActionObjectView):
# 	model= UnitRole