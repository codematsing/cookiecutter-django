from django.urls import path, include
from .views import (
	{{cookiecutter.snake_case_model_name}}ListAjaxView,
	{{cookiecutter.snake_case_model_name}}CreateAjaxView,
	{{cookiecutter.snake_case_model_name}}DetailAjaxView,
	{{cookiecutter.snake_case_model_name}}UpdateAjaxView,
	{{cookiecutter.snake_case_model_name}}DeleteAjaxView,
    # {{cookiecutter.snake_case_model_name}}<snake_case_action>AjaxView,
    # {{cookiecutter.snake_case_model_name}}Add<snake_case_model_name_fk>AjaxView,
    # {{cookiecutter.snake_case_model_name}}Remove<snake_case_model_name_fk>AjaxView,
    # {{cookiecutter.snake_case_model_name}}<snake_case_action><snake_case_model_name_fk>AjaxView,
)

app_name = "{{cookiecutter.app_name}}_ajax"

urlpatterns = [
    # add
    path(
        "list/",
        {{cookiecutter.snake_case_model_name}}ListAjaxView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        {{cookiecutter.snake_case_model_name}}CreateAjaxView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        {{cookiecutter.snake_case_model_name}}DetailAjaxView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        {{cookiecutter.snake_case_model_name}}UpdateAjaxView.as_view(),
        name="update"
    ),
    # # delete
    # path(
    #     "<int:pk>/delete/",
    #     {{cookiecutter.snake_case_model_name}}DeleteAjaxView.as_view(),
    #     "delete"
    # ),
    # # actions
    # path(
    #     "<int:pk>/<action>/",
    #     {{cookiecutter.snake_case_model_name}}<snake_case_action>AjaxView.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<dtype:arg_fk>",
    #     {{cookiecutter.snake_case_model_name}}Add<snake_case_model_name_fk>AjaxView.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<dtype:arg_fk>",
    #     {{cookiecutter.snake_case_model_name}}Remove<snake_case_model_name_fk>AjaxView.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<dtype:arg_fk>",
    #     {{cookiecutter.snake_case_model_name}}<snake_case_action><snake_case_model_name_fk>AjaxView.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
]
