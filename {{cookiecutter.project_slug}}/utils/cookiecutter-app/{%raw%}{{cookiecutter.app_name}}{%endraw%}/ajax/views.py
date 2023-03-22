{% raw %}
from django.shortcuts import render
from {{cookiecutter.app_name}}.models import {{cookiecutter.snake_case_model_name}}
from utils.views.ajax import (
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

class {{cookiecutter.snake_case_model_name}}ListAjaxView(BaseListAjaxView):
	model = {{cookiecutter.snake_case_model_name}}

class {{cookiecutter.snake_case_model_name}}CreateAjaxView(BaseCreateAjaxView):
	model = {{cookiecutter.snake_case_model_name}}

class {{cookiecutter.snake_case_model_name}}DetailAjaxView(BaseDetailAjaxView):
	model = {{cookiecutter.snake_case_model_name}}

class {{cookiecutter.snake_case_model_name}}UpdateAjaxView(BaseUpdateAjaxView):
	model = {{cookiecutter.snake_case_model_name}}

class {{cookiecutter.snake_case_model_name}}DeleteAjaxView(BaseDeleteAjaxView):
	model = {{cookiecutter.snake_case_model_name}}

class {{cookiecutter.snake_case_model_name}}<snake_case_action>AjaxView(BaseActionAjaxView):
	model = {{cookiecutter.snake_case_model_name}}

class {{cookiecutter.snake_case_model_name}}Add<snake_case_model_name_fk>AjaxView(BaseAddObjectAjaxView):
	model = {{cookiecutter.snake_case_model_name}}

class {{cookiecutter.snake_case_model_name}}Remove<snake_case_model_name_fk>AjaxView(BaseRemoveObjectAjaxView):
	model = {{cookiecutter.snake_case_model_name}}

class {{cookiecutter.snake_case_model_name}}<snake_case_action><snake_case_model_name_fk>AjaxView(BaseActionObjectAjaxView):
	model = {{cookiecutter.snake_case_model_name}}
{% endraw %}