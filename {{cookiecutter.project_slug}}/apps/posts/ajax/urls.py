from django.urls import path, include
from .views import (
	PostListAjaxView,
	PostCreateAjaxView,
	PostDetailAjaxView,
	PostUpdateAjaxView,
	PostDeleteAjaxView,
    # Post<snake_case_action>AjaxView,
    # PostAdd<snake_case_model_name_fk>AjaxView,
    # PostRemove<snake_case_model_name_fk>AjaxView,
    # Post<snake_case_action><snake_case_model_name_fk>AjaxView,
)

app_name = "posts_ajax"

urlpatterns = [
    # add
    path(
        "list/",
        PostListAjaxView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        PostCreateAjaxView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        PostDetailAjaxView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        PostUpdateAjaxView.as_view(),
        name="update"
    ),
    # # delete
    # path(
    #     "<int:pk>/delete/",
    #     PostDeleteAjaxView.as_view(),
    #     "delete"
    # ),
    # # actions
    # path(
    #     "<int:pk>/<action>/",
    #     Post<snake_case_action>AjaxView.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<dtype:arg_fk>",
    #     PostAdd<snake_case_model_name_fk>AjaxView.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<dtype:arg_fk>",
    #     PostRemove<snake_case_model_name_fk>AjaxView.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<dtype:arg_fk>",
    #     Post<snake_case_action><snake_case_model_name_fk>AjaxView.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
]
