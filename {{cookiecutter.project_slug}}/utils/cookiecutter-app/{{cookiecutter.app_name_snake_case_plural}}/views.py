from django.shortcuts import render
from .models import {{cookiecutter.model_name_camel_case}}
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
class {{cookiecutter.model_name_camel_case}}ListView({{cookiecutter.view_prefix}}ListView):
	model = {{cookiecutter.model_name_camel_case}}

class {{cookiecutter.model_name_camel_case}}CreateView({{cookiecutter.view_prefix}}CreateView):
	model = {{cookiecutter.model_name_camel_case}}

class {{cookiecutter.model_name_camel_case}}DetailView({{cookiecutter.view_prefix}}DetailView):
	model = {{cookiecutter.model_name_camel_case}}

class {{cookiecutter.model_name_camel_case}}UpdateView({{cookiecutter.view_prefix}}UpdateView):
	model = {{cookiecutter.model_name_camel_case}}

class {{cookiecutter.model_name_camel_case}}DeleteView({{cookiecutter.view_prefix}}DeleteView):
	model = {{cookiecutter.model_name_camel_case}}

# class {{cookiecutter.model_name_camel_case}}<snake_case_action>View(BaseActionView):
# 	model= {{cookiecutter.model_name_camel_case}}

# class {{cookiecutter.model_name_camel_case}}Add<model_name_camel_case_fk>View(BaseAddObjectView):
# 	model= {{cookiecutter.model_name_camel_case}}

# class {{cookiecutter.model_name_camel_case}}Remove<model_name_camel_case_fk>View(BaseRemoveObjectView):
# 	model= {{cookiecutter.model_name_camel_case}}

# class {{cookiecutter.model_name_camel_case}}<snake_case_action><model_name_camel_case_fk>View(BaseActionObjectView):
# 	model= {{cookiecutter.model_name_camel_case}}