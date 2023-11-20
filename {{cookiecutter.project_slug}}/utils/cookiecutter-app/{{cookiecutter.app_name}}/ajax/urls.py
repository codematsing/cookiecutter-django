from django.urls import path, include
from .views import (
	{{cookiecutter.camel_case_model_name}}ListAjaxView,
	{{cookiecutter.camel_case_model_name}}CreateAjaxView,
	{{cookiecutter.camel_case_model_name}}DetailAjaxView,
	{{cookiecutter.camel_case_model_name}}UpdateAjaxView,
	{{cookiecutter.camel_case_model_name}}DeleteAjaxView,
    # {{cookiecutter.camel_case_model_name}}<snake_case_action>AjaxView,
    # {{cookiecutter.camel_case_model_name}}Add<camel_case_model_name_fk>AjaxView,
    # {{cookiecutter.camel_case_model_name}}Remove<camel_case_model_name_fk>AjaxView,
    # {{cookiecutter.camel_case_model_name}}<snake_case_action><camel_case_model_name_fk>AjaxView,
)

app_name = "{{cookiecutter.app_name}}_ajax"

urlpatterns = [
    # add
    path(
        "list/",
        {{cookiecutter.camel_case_model_name}}ListAjaxView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        {{cookiecutter.camel_case_model_name}}CreateAjaxView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        {{cookiecutter.camel_case_model_name}}DetailAjaxView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        {{cookiecutter.camel_case_model_name}}UpdateAjaxView.as_view(),
        name="update"
    ),
    # # delete
    # path(
    #     "<int:pk>/delete/",
    #     {{cookiecutter.camel_case_model_name}}DeleteAjaxView.as_view(),
    #     "delete"
    # ),
    # # actions
    # path(
    #     "<int:pk>/<action>/",
    #     {{cookiecutter.camel_case_model_name}}<snake_case_action>AjaxView.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<dtype:arg_fk>",
    #     {{cookiecutter.camel_case_model_name}}Add<camel_case_model_name_fk>AjaxView.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<dtype:arg_fk>",
    #     {{cookiecutter.camel_case_model_name}}Remove<camel_case_model_name_fk>AjaxView.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<dtype:arg_fk>",
    #     {{cookiecutter.camel_case_model_name}}<snake_case_action><camel_case_model_name_fk>AjaxView.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
]
