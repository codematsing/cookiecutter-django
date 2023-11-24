from django.apps import AppConfig


class TagsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tags'

    def ready(self):
        try:
            import tags.signals  # noqa F401
        except ImportError:
            pass