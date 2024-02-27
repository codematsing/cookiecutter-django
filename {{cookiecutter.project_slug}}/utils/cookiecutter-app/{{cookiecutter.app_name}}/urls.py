from django.urls import path, include
from .views import (
{{cookiecutter.camel_case_model_name}}ListView,
{{cookiecutter.camel_case_model_name}}CreateView,
{{cookiecutter.camel_case_model_name}}DetailView,
{{cookiecutter.camel_case_model_name}}UpdateView,
{{cookiecutter.camel_case_model_name}}DeleteView,
# {{cookiecutter.camel_case_model_name}}<snake_case_action>View,
# {{cookiecutter.camel_case_model_name}}Add<camel_case_model_name_fk>View,
# {{cookiecutter.camel_case_model_name}}Remove<camel_case_model_name_fk>View,
# {{cookiecutter.camel_case_model_name}}<snake_case_action><camel_case_model_name_fk>View,
)

app_name = "{{cookiecutter.app_name}}"

# Make sure you add urls to model.spy
# add get_<name>_url() method

urlpatterns = [
    # list
    path(
        "",
        {{cookiecutter.camel_case_model_name}}ListView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        {{cookiecutter.camel_case_model_name}}CreateView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        {{cookiecutter.camel_case_model_name}}DetailView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        {{cookiecutter.camel_case_model_name}}UpdateView.as_view(),
        name="update"
    ),
    # delete
    path(
        "<int:pk>/delete/",
        {{cookiecutter.camel_case_model_name}}DeleteView.as_view(),
        name="delete"
    ),
    # actions
    # path(
    #     "<int:pk>/<action>/",
    #     {{cookiecutter.camel_case_model_name}}<snake_case_action>View.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<int:pk_fk>",
    #     {{cookiecutter.camel_case_model_name}}Add<camel_case_model_name_fk>View.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<int:pk_fk>",
    #     {{cookiecutter.camel_case_model_name}}Remove<camel_case_model_name_fk>View.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<int:pk_fk>",
    #     {{cookiecutter.camel_case_model_name}}<snake_case_action><camel_case_model_name_fk>View.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
    path(
        "ajax/",
        include("{{cookiecutter.app_name}}.ajax.urls",
        namespace="ajax")
    ),
]