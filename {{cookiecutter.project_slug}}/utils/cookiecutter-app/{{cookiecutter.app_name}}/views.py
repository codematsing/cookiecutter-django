from django.shortcuts import render
from .models import {{cookiecutter.camel_case_model_name}}
from utils.base_views.views import (
	{% if cookiecutter.view_prefix =="Base" %}
	BaseListView,
	BaseCreateView,
	BaseDetailView,
	BaseUpdateView,

	{% endif %}
	BaseDeleteView,
	BaseActionView,
	BaseAddObjectView,
	BaseRemoveObjectView,
	BaseActionObjectView,
)
{% if cookiecutter.view_prefix=="Admin" %}
from utils.base_views.admin_views import (
	AdminListView,
	AdminCreateView,
	AdminDetailView,
	AdminUpdateView,
	AdminDeleteView
)
{% elif cookiecutter.view_prefix=="Public" %}
from utils.base_views.public_views import (
	PublicListView,
	PublicCreateView,
	PublicDetailView,
	PublicUpdateView,
)

{% endif %}

import logging
logger = logging.getLogger(__name__)

# Create your views here.
class {{cookiecutter.camel_case_model_name}}ListView({{cookiecutter.view_prefix}}ListView):
	model = {{cookiecutter.camel_case_model_name}}

class {{cookiecutter.camel_case_model_name}}CreateView({{cookiecutter.view_prefix}}CreateView):
	model = {{cookiecutter.camel_case_model_name}}

class {{cookiecutter.camel_case_model_name}}DetailView({{cookiecutter.view_prefix}}DetailView):
	model = {{cookiecutter.camel_case_model_name}}

class {{cookiecutter.camel_case_model_name}}UpdateView({{cookiecutter.view_prefix}}UpdateView):
	model = {{cookiecutter.camel_case_model_name}}

class {{cookiecutter.camel_case_model_name}}DeleteView({{cookiecutter.view_prefix}}DeleteView):
	model = {{cookiecutter.camel_case_model_name}}

class {{cookiecutter.camel_case_model_name}}AutocompleteView(BaseAutocompleteView):
	model = {{cookiecutter.camel_case_model_name}}

# class {{cookiecutter.camel_case_model_name}}<snake_case_action>View(BaseActionView):
# 	model= {{cookiecutter.camel_case_model_name}}

# class {{cookiecutter.camel_case_model_name}}Add<camel_case_model_name_fk>View(BaseAddObjectView):
# 	model= {{cookiecutter.camel_case_model_name}}

# class {{cookiecutter.camel_case_model_name}}Remove<camel_case_model_name_fk>View(BaseRemoveObjectView):
# 	model= {{cookiecutter.camel_case_model_name}}

# class {{cookiecutter.camel_case_model_name}}<snake_case_action><camel_case_model_name_fk>View(BaseActionObjectView):
# 	model= {{cookiecutter.camel_case_model_name}}