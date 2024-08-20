from django.apps import AppConfig


class VerificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auxiliaries.verification'

    def ready(self):
        try:
           import auxiliaries.verification.signals
        except ImportError:
            pass
