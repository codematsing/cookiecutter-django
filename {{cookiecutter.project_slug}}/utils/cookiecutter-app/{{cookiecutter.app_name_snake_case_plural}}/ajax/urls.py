from django.urls import path, include
from .views import (
	{{cookiecutter.model_name_camel_case}}ListAjaxView,
	{{cookiecutter.model_name_camel_case}}CreateAjaxView,
	{{cookiecutter.model_name_camel_case}}DetailAjaxView,
	{{cookiecutter.model_name_camel_case}}UpdateAjaxView,
	{{cookiecutter.model_name_camel_case}}DeleteAjaxView,
    # {{cookiecutter.model_name_camel_case}}<snake_case_action>AjaxView,
    # {{cookiecutter.model_name_camel_case}}Add<model_name_camel_case_fk>AjaxView,
    # {{cookiecutter.model_name_camel_case}}Remove<model_name_camel_case_fk>AjaxView,
    # {{cookiecutter.model_name_camel_case}}<snake_case_action><model_name_camel_case_fk>AjaxView,
)

app_name = "{{cookiecutter.app_name_snake_case_plural}}_ajax"

urlpatterns = [
    # add
    path(
        "list/",
        {{cookiecutter.model_name_camel_case}}ListAjaxView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        {{cookiecutter.model_name_camel_case}}CreateAjaxView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        {{cookiecutter.model_name_camel_case}}DetailAjaxView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        {{cookiecutter.model_name_camel_case}}UpdateAjaxView.as_view(),
        name="update"
    ),
    # # delete
    # path(
    #     "<int:pk>/delete/",
    #     {{cookiecutter.model_name_camel_case}}DeleteAjaxView.as_view(),
    #     "delete"
    # ),
    # # actions
    # path(
    #     "<int:pk>/<action>/",
    #     {{cookiecutter.model_name_camel_case}}<snake_case_action>AjaxView.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<dtype:arg_fk>",
    #     {{cookiecutter.model_name_camel_case}}Add<model_name_camel_case_fk>AjaxView.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<dtype:arg_fk>",
    #     {{cookiecutter.model_name_camel_case}}Remove<model_name_camel_case_fk>AjaxView.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<dtype:arg_fk>",
    #     {{cookiecutter.model_name_camel_case}}<snake_case_action><model_name_camel_case_fk>AjaxView.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
]
