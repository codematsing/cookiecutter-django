from django.urls import path, include
from .views import (
	GuidelineListAjaxView,
	GuidelineCreateAjaxView,
	GuidelineDetailAjaxView,
	GuidelineUpdateAjaxView,
	GuidelineDeleteAjaxView,
    # Guideline<snake_case_action>AjaxView,
    # GuidelineAdd<model_name_camel_case_fk>AjaxView,
    # GuidelineRemove<model_name_camel_case_fk>AjaxView,
    # Guideline<snake_case_action><model_name_camel_case_fk>AjaxView,
)

app_name = "guidelines_ajax"

urlpatterns = [
    # add
    path(
        "list/",
        GuidelineListAjaxView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        GuidelineCreateAjaxView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        GuidelineDetailAjaxView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        GuidelineUpdateAjaxView.as_view(),
        name="update"
    ),
    # # delete
    # path(
    #     "<int:pk>/delete/",
    #     GuidelineDeleteAjaxView.as_view(),
    #     "delete"
    # ),
    # # actions
    # path(
    #     "<int:pk>/<action>/",
    #     Guideline<snake_case_action>AjaxView.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<dtype:arg_fk>",
    #     GuidelineAdd<model_name_camel_case_fk>AjaxView.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<dtype:arg_fk>",
    #     GuidelineRemove<model_name_camel_case_fk>AjaxView.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<dtype:arg_fk>",
    #     Guideline<snake_case_action><model_name_camel_case_fk>AjaxView.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
]
