from django.apps import AppConfig


class {{cookiecutter.camel_case_app_name}}AjaxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{{cookiecutter.app_location}}_ajax'