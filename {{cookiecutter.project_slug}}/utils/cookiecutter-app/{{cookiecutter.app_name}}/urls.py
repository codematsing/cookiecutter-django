from django.urls import path, include
from .views import (
{{cookiecutter.model_name_camel_case}}ListView,
{{cookiecutter.model_name_camel_case}}CreateView,
{{cookiecutter.model_name_camel_case}}DetailView,
{{cookiecutter.model_name_camel_case}}UpdateView,
{{cookiecutter.model_name_camel_case}}DeleteView,
# {{cookiecutter.model_name_camel_case}}<snake_case_action>View,
# {{cookiecutter.model_name_camel_case}}Add<model_name_camel_case_fk>View,
# {{cookiecutter.model_name_camel_case}}Remove<model_name_camel_case_fk>View,
# {{cookiecutter.model_name_camel_case}}<snake_case_action><model_name_camel_case_fk>View,
)

app_name_snake_case_plural = "{{cookiecutter.app_name_snake_case_plural}}"

# Make sure you add urls to model.spy
# add get_<name>_url() method

urlpatterns = [
    # list
    path(
        "",
        {{cookiecutter.model_name_camel_case}}ListView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        {{cookiecutter.model_name_camel_case}}CreateView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        {{cookiecutter.model_name_camel_case}}DetailView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        {{cookiecutter.model_name_camel_case}}UpdateView.as_view(),
        name="update"
    ),
    # delete
    path(
        "<int:pk>/delete/",
        {{cookiecutter.model_name_camel_case}}DeleteView.as_view(),
        name="delete"
    ),
    # actions
    # path(
    #     "<int:pk>/<action>/",
    #     {{cookiecutter.model_name_camel_case}}<snake_case_action>View.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<int:pk_fk>",
    #     {{cookiecutter.model_name_camel_case}}Add<model_name_camel_case_fk>View.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<int:pk_fk>",
    #     {{cookiecutter.model_name_camel_case}}Remove<model_name_camel_case_fk>View.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<int:pk_fk>",
    #     {{cookiecutter.model_name_camel_case}}<snake_case_action><model_name_camel_case_fk>View.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
    path(
        "ajax/",
        include("{{cookiecutter.app_name_snake_case_plural}}.ajax.urls",
        namespace="ajax")
    ),
]