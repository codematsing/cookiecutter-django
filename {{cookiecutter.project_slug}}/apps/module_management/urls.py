from django.urls import path, include
from .views import (
ModuleManagementListView,
ModuleManagementCreateView,
ModuleManagementDetailView,
ModuleManagementUpdateView,
ModuleManagementDeleteView,
# ModuleManagement<snake_case_action>View,
# ModuleManagementAdd<model_name_camel_case_fk>View,
# ModuleManagementRemove<model_name_camel_case_fk>View,
# ModuleManagement<snake_case_action><model_name_camel_case_fk>View,
)

app_name = "module_management"

# Make sure you add urls to model.spy
# add get_<name>_url() method

urlpatterns = [
    # list
    path(
        "",
        ModuleManagementListView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        ModuleManagementCreateView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        ModuleManagementDetailView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        ModuleManagementUpdateView.as_view(),
        name="update"
    ),
    # delete
    path(
        "<int:pk>/delete/",
        ModuleManagementDeleteView.as_view(),
        name="delete"
    ),
    # actions
    # path(
    #     "<int:pk>/<action>/",
    #     ModuleManagement<snake_case_action>View.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<int:pk_fk>",
    #     ModuleManagementAdd<model_name_camel_case_fk>View.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<int:pk_fk>",
    #     ModuleManagementRemove<model_name_camel_case_fk>View.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<int:pk_fk>",
    #     ModuleManagement<snake_case_action><model_name_camel_case_fk>View.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
    path(
        "ajax/",
        include("module_management.ajax.urls",
        namespace="ajax")
    ),
]