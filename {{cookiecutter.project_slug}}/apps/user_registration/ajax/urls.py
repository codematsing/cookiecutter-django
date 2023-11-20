from django.urls import path, include
from .views import (
	RegistrationListAjaxView,
	RegistrationCreateAjaxView,
	RegistrationDetailAjaxView,
	RegistrationUpdateAjaxView,
	RegistrationDeleteAjaxView,
)

app_name = "user_registration_ajax"

urlpatterns = [
    path(
        "list/",
        RegistrationListAjaxView.as_view(),
        name="list"
    ),

    # detail
    path(
        "<int:pk>/",
        RegistrationDetailAjaxView.as_view(),
        name="detail"
    ),
    # update
    # path(
    #     "<int:pk>/edit/",
    #     RegistrationUpdateAjaxView.as_view(),
    #     name="update"
    # ),
    # delete
    # path(
    #     "<int:pk>/delete/",
    #     RegistrationDeleteAjaxView.as_view(),
    #     "delete"
    # ),
    # # actions
    # path(
    #     "<int:pk>/approve",
    #     RegistrationApproveAjaxView.as_view(),
    #     "approve"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<dtype:arg_fk>",
    #     RegistrationAdd<snake_case_model_name_fk>AjaxView.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<dtype:arg_fk>",
    #     RegistrationRemove<snake_case_model_name_fk>AjaxView.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<dtype:arg_fk>",
    #     Registration<snake_case_action><snake_case_model_name_fk>AjaxView.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
]
