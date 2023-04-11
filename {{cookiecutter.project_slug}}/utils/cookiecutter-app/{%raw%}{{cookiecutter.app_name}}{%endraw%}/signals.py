from django.db.models.signals import post_save
from django.dispatch import receiver
from {{cookiecutter.app_name}}.models import {{cookiecutter.snake_case_model_name}}

# @receiver(post_save, sender={{cookiecutter.snake_case_model_name}})
# def {{cookiecutter.model_name[:-1]}}_saved(sender, instance, created, **kwargs):
#     if created:
#         pass
#     else:
#         pass