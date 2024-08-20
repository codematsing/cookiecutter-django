from django.shortcuts import render
from .models import Guideline
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

from guidelines.forms import GuidelineForm


import logging
logger = logging.getLogger(__name__)

# Create your views here.
class GuidelineListView(AdminListView):
	model = Guideline

class GuidelineCreateView(AdminCreateView):
	model = Guideline
	form_class = GuidelineForm

class GuidelineDetailView(AdminDetailView):
	model = Guideline

class GuidelineUpdateView(AdminUpdateView):
	model = Guideline
	form_class = GuidelineForm

class GuidelineDeleteView(AdminDeleteView):
	model = Guideline

# class Guideline<snake_case_action>View(BaseActionView):
# 	model= Guideline

# class GuidelineAdd<model_name_camel_case_fk>View(BaseAddObjectView):
# 	model= Guideline

# class GuidelineRemove<model_name_camel_case_fk>View(BaseRemoveObjectView):
# 	model= Guideline

# class Guideline<snake_case_action><model_name_camel_case_fk>View(BaseActionObjectView):
# 	model= Guideline