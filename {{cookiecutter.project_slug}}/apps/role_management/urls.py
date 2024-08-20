from django.urls import path, include
from .views import (
RoleListView,
RoleCreateView,
RoleDetailView,
RoleUpdateView,
RoleDeleteView,
# Role<snake_case_action>View,
# RoleAdd<model_name_camel_case_fk>View,
# RoleRemove<model_name_camel_case_fk>View,
# Role<snake_case_action><model_name_camel_case_fk>View,
)

app_name = "role_management"

# Make sure you add urls to model.spy
# add get_<name>_url() method

urlpatterns = [
    # list
    path(
        "",
        RoleListView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        RoleCreateView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        RoleDetailView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        RoleUpdateView.as_view(),
        name="update"
    ),
    # delete
    path(
        "<int:pk>/delete/",
        RoleDeleteView.as_view(),
        name="delete"
    ),
    # actions
    # path(
    #     "<int:pk>/<action>/",
    #     Role<snake_case_action>View.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<int:pk_fk>",
    #     RoleAdd<model_name_camel_case_fk>View.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<int:pk_fk>",
    #     RoleRemove<model_name_camel_case_fk>View.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<int:pk_fk>",
    #     Role<snake_case_action><model_name_camel_case_fk>View.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
    path(
        "ajax/",
        include("role_management.ajax.urls",
        namespace="ajax")
    ),
]