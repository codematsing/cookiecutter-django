from django.urls import path, include
from .views import (
VerificationListView,
VerificationCreateView,
VerificationDetailView,
VerificationUpdateView,
VerificationDeleteView,
# Verification<snake_case_action>View,
# VerificationAdd<snake_case_model_name_fk>View,
# VerificationRemove<snake_case_model_name_fk>View,
# Verification<snake_case_action><snake_case_model_name_fk>View,
)

app_name = "verification"

urlpatterns = [
    # list
    path(
        "",
        VerificationListView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        VerificationCreateView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        VerificationDetailView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        VerificationUpdateView.as_view(),
        name="update"
    ),
    # delete
    path(
        "<int:pk>/delete/",
        VerificationDeleteView.as_view(),
        name="delete"
    ),
    # actions
    # path(
    #     "<int:pk>/<action>/",
    #     Verification<snake_case_action>View.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<int:pk_fk>",
    #     VerificationAdd<snake_case_model_name_fk>View.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<int:pk_fk>",
    #     VerificationRemove<snake_case_model_name_fk>View.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<int:pk_fk>",
    #     Verification<snake_case_action><snake_case_model_name_fk>View.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
    path(
        "ajax/",
        include("verification.ajax.urls",
        namespace="ajax")
    ),
]