from django.urls import path, include
from .views import (
	UnitRoleListAjaxView,
	UnitRoleCreateAjaxView,
	UnitRoleDetailAjaxView,
	UnitRoleUpdateAjaxView,
	UnitRoleDeleteAjaxView,
    # UnitRole<snake_case_action>AjaxView,
    # UnitRoleAdd<model_name_camel_case_fk>AjaxView,
    # UnitRoleRemove<model_name_camel_case_fk>AjaxView,
    # UnitRole<snake_case_action><model_name_camel_case_fk>AjaxView,
)

app_name = "unit_roles_ajax"

urlpatterns = [
    # add
    path(
        "list/",
        UnitRoleListAjaxView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        UnitRoleCreateAjaxView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        UnitRoleDetailAjaxView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        UnitRoleUpdateAjaxView.as_view(),
        name="update"
    ),
    # # delete
    # path(
    #     "<int:pk>/delete/",
    #     UnitRoleDeleteAjaxView.as_view(),
    #     "delete"
    # ),
    # # actions
    # path(
    #     "<int:pk>/<action>/",
    #     UnitRole<snake_case_action>AjaxView.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<dtype:arg_fk>",
    #     UnitRoleAdd<model_name_camel_case_fk>AjaxView.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<dtype:arg_fk>",
    #     UnitRoleRemove<model_name_camel_case_fk>AjaxView.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<dtype:arg_fk>",
    #     UnitRole<snake_case_action><model_name_camel_case_fk>AjaxView.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
]
