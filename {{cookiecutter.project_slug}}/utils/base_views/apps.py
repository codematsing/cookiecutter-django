from django.apps import AppConfig


class BaseViewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_views'
