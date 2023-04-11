from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from {{cookiecutter.app_name}}.models import {{cookiecutter.snake_case_model_name}}

# @receiver(post_save, sender={{cookiecutter.snake_case_model_name}})
# def {{cookiecutter.model_name[:-1]}}_saved(sender, instance, created, **kwargs):
#     if created:
#         pass
#     else:
#         pass

# @receiver(m2m_changed, sender={{cookiecutter.snake_case_model_name}}.<model_fk>.through)
# def {{cookiecutter.model_name[:-1]}}_<model_fk>_changed(sender, instance, action, reverse, model, pk_set, using):
#     if action=='post_add':
#         pass
#     elif action=='post_remove':
#         pass