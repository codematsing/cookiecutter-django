from django.shortcuts import render
from guidelines.models import Guideline
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

class GuidelineListAjaxView(BaseListAjaxView):
	column_defs = [
		{'name':'href'},
		{'name':'content'},
		{'name':'status'},
	]
	initial_order=[["status", "asc"]]

	model = Guideline

class GuidelineCreateAjaxView(BaseCreateAjaxView):
	model = Guideline

class GuidelineDetailAjaxView(BaseDetailAjaxView):
	model = Guideline

class GuidelineUpdateAjaxView(BaseUpdateAjaxView):
	model = Guideline

class GuidelineDeleteAjaxView(BaseDeleteAjaxView):
	model = Guideline

# class Guideline<snake_case_action>AjaxView(BaseActionAjaxView):
# 	model = Guideline

# class GuidelineAdd<model_name_camel_case_fk>AjaxView(BaseAddObjectAjaxView):
# 	model = Guideline

# class GuidelineRemove<model_name_camel_case_fk>AjaxView(BaseRemoveObjectAjaxView):
# 	model = Guideline

# class Guideline<snake_case_action><model_name_camel_case_fk>AjaxView(BaseActionObjectAjaxView):
# 	model = Guideline