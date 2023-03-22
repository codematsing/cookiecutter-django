{% raw %}
from django.apps import AppConfig


class {{cookiecutter.snake_case_app_name}}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{{cookiecutter.app_name}}'

    def ready(self):
        try:
           import {{cookiecutter.app_name}}.signals
        except ImportError:
            pass

{% endraw %}