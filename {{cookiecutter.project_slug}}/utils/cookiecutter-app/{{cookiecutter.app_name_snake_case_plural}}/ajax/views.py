from django.shortcuts import render
from {{cookiecutter.app_name_snake_case_plural}}.models import {{cookiecutter.model_name_camel_case}}
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

class {{cookiecutter.model_name_camel_case}}ListAjaxView(BaseListAjaxView):
	model = {{cookiecutter.model_name_camel_case}}

class {{cookiecutter.model_name_camel_case}}CreateAjaxView(BaseCreateAjaxView):
	model = {{cookiecutter.model_name_camel_case}}

class {{cookiecutter.model_name_camel_case}}DetailAjaxView(BaseDetailAjaxView):
	model = {{cookiecutter.model_name_camel_case}}

class {{cookiecutter.model_name_camel_case}}UpdateAjaxView(BaseUpdateAjaxView):
	model = {{cookiecutter.model_name_camel_case}}

class {{cookiecutter.model_name_camel_case}}DeleteAjaxView(BaseDeleteAjaxView):
	model = {{cookiecutter.model_name_camel_case}}

# class {{cookiecutter.model_name_camel_case}}<snake_case_action>AjaxView(BaseActionAjaxView):
# 	model = {{cookiecutter.model_name_camel_case}}

# class {{cookiecutter.model_name_camel_case}}Add<model_name_camel_case_fk>AjaxView(BaseAddObjectAjaxView):
# 	model = {{cookiecutter.model_name_camel_case}}

# class {{cookiecutter.model_name_camel_case}}Remove<model_name_camel_case_fk>AjaxView(BaseRemoveObjectAjaxView):
# 	model = {{cookiecutter.model_name_camel_case}}

# class {{cookiecutter.model_name_camel_case}}<snake_case_action><model_name_camel_case_fk>AjaxView(BaseActionObjectAjaxView):
# 	model = {{cookiecutter.model_name_camel_case}}