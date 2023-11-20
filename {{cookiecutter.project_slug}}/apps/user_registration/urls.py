from django.urls import path, include

from .views import (
    RegistrationListView,
    RegistrationCreateView,
    RegistrationDetailView,
    RegistrationUpdateView,
    RegistrationDeleteView,
    RegistrationApproveView,
    RegistrationRejectView,
)

app_name = "user_registration"

urlpatterns = [
    # list
    path(
        "",
        RegistrationListView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        RegistrationCreateView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        RegistrationDetailView.as_view(),
        name="detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        RegistrationUpdateView.as_view(),
        name="update"
    ),
    # delete
    path(
        "<int:pk>/delete/",
        RegistrationDeleteView.as_view(),
        name="delete"
    ),
    path(
        "<int:pk>/approve/",
        RegistrationApproveView.as_view(),
        name="approve"
    ),
    path(
        "<int:pk>/reject/",
        RegistrationRejectView.as_view(),
        name="reject"
    ),
    # actions
    # path(
    #     "<int:pk>/<action>/",
    #     Registration<snake_case_action>View.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<int:pk_fk>",
    #     RegistrationAdd<snake_case_model_name_fk>View.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # remove
    # path(
    #     "<int:pk>/remove/<int:pk_fk>",
    #     RegistrationRemove<snake_case_model_name_fk>View.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<int:pk_fk>",
    #     Registration<snake_case_action><snake_case_model_name_fk>View.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
    path(
        "ajax/",
        include("user_registration.ajax.urls",
        namespace="ajax")
    ),
]
