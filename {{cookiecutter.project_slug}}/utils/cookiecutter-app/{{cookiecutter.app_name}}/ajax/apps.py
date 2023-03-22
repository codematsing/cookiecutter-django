from django.apps import AppConfig


class {{cookiecutter.snake_case_app_name}}AjaxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{{cookiecutter.app_name}}_ajax'
