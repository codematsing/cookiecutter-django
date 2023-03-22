{% raw %}
from django.urls import path, include
from views import (
{{cookiecutter.snake_case_model_name}}ListView,
{{cookiecutter.snake_case_model_name}}DetailView,
{{cookiecutter.snake_case_model_name}}UpdateView,
{{cookiecutter.snake_case_model_name}}DeleteView,
# {{cookiecutter.snake_case_model_name}}<snake_case_action>View,
# {{cookiecutter.snake_case_model_name}}Add<snake_case_model_name_fk>View,
# {{cookiecutter.snake_case_model_name}}Remove<snake_case_model_name_fk>View,
# {{cookiecutter.snake_case_model_name}}<snake_case_action><snake_case_model_name_fk>View,
)

app_name = "{{cookiecutter.app_name}}"

urlpatterns = [
    path('ajax/', "{{cookiecutter.app_name}}.ajax.urls", name='ajax'),
]
url_patterns = [
    # list
    path(
        "",
        {{cookiecutter.snake_case_model_name}}ListView.as_view(),
        name="list"
    ),
    # create
    path(
        "new/",
        {{cookiecutter.snake_case_model_name}}CreateView.as_view(),
        name="create"
    ),
    # detail
    path(
        "<int:pk>/",
        {{cookiecutter.snake_case_model_name}}DetailView.as_view(),
        "detail"
    ),
    # update
    path(
        "<int:pk>/edit/",
        {{cookiecutter.snake_case_model_name}}UpdateView.as_view(),
        "update"
    ),
    # delete
    path(
        "<int:pk>/delete/",
        {{cookiecutter.snake_case_model_name}}DeleteView.as_view(),
        "delete"
    ),
    # actions
    # path(
    #     "<int:pk>/<action>/",
    #     {{cookiecutter.snake_case_model_name}}<snake_case_action>View.as_view(),
    #     "<action>"
    # ),
    # # add
    # path(
    #     "<int:pk>/add/<int:pk_fk>",
    #     {{cookiecutter.snake_case_model_name}}Add<snake_case_model_name_fk>View.as_view(),
    #     "add_<model_name_fk>"
    # ),
    # # remove
    # path(
    #     "<int:pk>/remove/<int:pk_fk>",
    #     {{cookiecutter.snake_case_model_name}}Remove<snake_case_model_name_fk>View.as_view(),
    #     "remove_<model_name_fk>"
    # ),
    # # model_fk model actions
    # path(
    #     "<int:pk>/<action>/<int:pk_fk>",
    #     {{cookiecutter.snake_case_model_name}}<snake_case_action><snake_case_model_name_fk>View.as_view(),
    #     "<action>_<model_name_fk>"
    # ),
    path(
        "ajax/",
        include(apps.ajax.urls,
        namespace="ajax")
    )
]

{% endraw %}