{% raw %}
from django.shortcuts import render
from models import {{cookiecutter.snake_case_model_name}}
from utils.base_views.views import (
	BaseListView,
	BaseCreateView,
	BaseDetailView,
	BaseUpdateView,
	BaseDeleteView,
	BaseActionView,
	BaseAddObjectView,
	BaseRemoveObjectView,
	BaseActionObjectView,
)

import logging
logger = logging.getLogger(__name__)

# Create your views here.
class {{cookiecutter.snake_case_model_name}}ListView(BaseListView):
	model = {{cookiecutter.snake_case_model_name}}

class {{cookiecutter.snake_case_model_name}}DetailView(BaseDetailView):
	model = {{cookiecutter.snake_case_model_name}}

class {{cookiecutter.snake_case_model_name}}UpdateView(BaseUpdateView):
	model = {{cookiecutter.snake_case_model_name}}

class {{cookiecutter.snake_case_model_name}}DeleteView(BaseDeleteView):
	model = {{cookiecutter.snake_case_model_name}}

class {{cookiecutter.snake_case_model_name}}DeleteView(BaseDeleteView):
	model = {{cookiecutter.snake_case_model_name}}

# class {{cookiecutter.snake_case_model_name}}<snake_case_action>View(BaseActionView):
# 	model= {{cookiecutter.snake_case_model_name}}

# class {{cookiecutter.snake_case_model_name}}Add<snake_case_model_name_fk>View(BaseAddObjectView):
# 	model= {{cookiecutter.snake_case_model_name}}

# class {{cookiecutter.snake_case_model_name}}Remove<snake_case_model_name_fk>View(BaseRemoveObjectView):
# 	model= {{cookiecutter.snake_case_model_name}}

# class {{cookiecutter.snake_case_model_name}}<snake_case_action><snake_case_model_name_fk>View(BaseActionObjectView):
# 	model= {{cookiecutter.snake_case_model_name}}
{% endraw %}