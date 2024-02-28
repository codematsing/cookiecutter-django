from django.apps import AppConfig


class {{cookiecutter.app_name_snake_case_plural_camel_case}}AjaxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{{cookiecutter.app_location_dot_notation}}_ajax'
