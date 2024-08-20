from django.urls import path, include
from .views import (
GuidelineListView,
GuidelineCreateView,
GuidelineDetailView,
GuidelineUpdateView,
GuidelineDeleteView,
# Guideline<snake_case_action>View,
# GuidelineAdd<model_name_camel_case_fk>View,
# GuidelineRemove<model_name_camel_case_fk>View,
# Guideline<snake_case_action><model_name_camel_case_fk>View,
)

app_name = "guidelines"

# Make sure you add urls to model.spy
# add get_<name>_url() method

urlpatterns = [
    # list
    path(
        "",
        GuidelineListView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        GuidelineCreateView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        GuidelineDetailView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        GuidelineUpdateView.as_view(),
        name="update"
    ),
    # delete
    path(
        "<int:pk>/delete/",
        GuidelineDeleteView.as_view(),
        name="delete"
    ),
    # actions
    # path(
    #     "<int:pk>/<action>/",
    #     Guideline<snake_case_action>View.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<int:pk_fk>",
    #     GuidelineAdd<model_name_camel_case_fk>View.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<int:pk_fk>",
    #     GuidelineRemove<model_name_camel_case_fk>View.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<int:pk_fk>",
    #     Guideline<snake_case_action><model_name_camel_case_fk>View.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
    path(
        "ajax/",
        include("guidelines.ajax.urls",
        namespace="ajax")
    ),
]