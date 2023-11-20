from django.apps import AppConfig


class {{cookiecutter.camel_case_app_name}}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{{cookiecutter.app_location}}'

    def ready(self):
        try:
           import {{cookiecutter.app_location}}.signals
        except ImportError:
            pass
