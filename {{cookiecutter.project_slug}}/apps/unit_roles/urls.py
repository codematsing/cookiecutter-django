from django.urls import path, include
from .views import (
UnitRoleListView,
UnitRoleCreateView,
UnitRoleDetailView,
UnitRoleUpdateView,
UnitRoleDeleteView,
# UnitRole<snake_case_action>View,
# UnitRoleAdd<model_name_camel_case_fk>View,
# UnitRoleRemove<model_name_camel_case_fk>View,
# UnitRole<snake_case_action><model_name_camel_case_fk>View,
)

app_name = "unit_roles"

# Make sure you add urls to model.spy
# add get_<name>_url() method

urlpatterns = [
    # list
    path(
        "",
        UnitRoleListView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        UnitRoleCreateView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        UnitRoleDetailView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        UnitRoleUpdateView.as_view(),
        name="update"
    ),
    # delete
    path(
        "<int:pk>/delete/",
        UnitRoleDeleteView.as_view(),
        name="delete"
    ),
    # actions
    # path(
    #     "<int:pk>/<action>/",
    #     UnitRole<snake_case_action>View.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<int:pk_fk>",
    #     UnitRoleAdd<model_name_camel_case_fk>View.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<int:pk_fk>",
    #     UnitRoleRemove<model_name_camel_case_fk>View.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<int:pk_fk>",
    #     UnitRole<snake_case_action><model_name_camel_case_fk>View.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
    path(
        "ajax/",
        include("unit_roles.ajax.urls",
        namespace="ajax")
    ),
]