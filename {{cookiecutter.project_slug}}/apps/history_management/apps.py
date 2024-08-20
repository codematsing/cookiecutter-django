from django.apps import AppConfig


class HistoryManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "history_management"

    def ready(self):
        try:
            import history_management.signals  # noqa F401
        except ImportError:
            pass

