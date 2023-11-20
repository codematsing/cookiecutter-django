from django.shortcuts import render
from {{cookiecutter.app_name}}.models import {{cookiecutter.camel_case_model_name}}
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

class {{cookiecutter.camel_case_model_name}}ListAjaxView(BaseListAjaxView):
	model = {{cookiecutter.camel_case_model_name}}

class {{cookiecutter.camel_case_model_name}}CreateAjaxView(BaseCreateAjaxView):
	model = {{cookiecutter.camel_case_model_name}}

class {{cookiecutter.camel_case_model_name}}DetailAjaxView(BaseDetailAjaxView):
	model = {{cookiecutter.camel_case_model_name}}

class {{cookiecutter.camel_case_model_name}}UpdateAjaxView(BaseUpdateAjaxView):
	model = {{cookiecutter.camel_case_model_name}}

class {{cookiecutter.camel_case_model_name}}DeleteAjaxView(BaseDeleteAjaxView):
	model = {{cookiecutter.camel_case_model_name}}

# class {{cookiecutter.camel_case_model_name}}<snake_case_action>AjaxView(BaseActionAjaxView):
# 	model = {{cookiecutter.camel_case_model_name}}

# class {{cookiecutter.camel_case_model_name}}Add<camel_case_model_name_fk>AjaxView(BaseAddObjectAjaxView):
# 	model = {{cookiecutter.camel_case_model_name}}

# class {{cookiecutter.camel_case_model_name}}Remove<camel_case_model_name_fk>AjaxView(BaseRemoveObjectAjaxView):
# 	model = {{cookiecutter.camel_case_model_name}}

# class {{cookiecutter.camel_case_model_name}}<snake_case_action><camel_case_model_name_fk>AjaxView(BaseActionObjectAjaxView):
# 	model = {{cookiecutter.camel_case_model_name}}