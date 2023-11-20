from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from utils import lambdas
from utils.base_models.models import AbstractAuditedModel
import os

# Create your models here.
class {{cookiecutter.camel_case_model_name}}Manager(models.Manager):
    pass

class {{cookiecutter.camel_case_model_name}}(AbstractAuditedModel):
    objects = {{cookiecutter.camel_case_model_name}}Manager()

    name = models.CharField(
        max_length=128, 
        blank=True, 
        null=True
    )
    # attachment = models.FileField(upload_to=lambdas.rename_upload)
    # uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT, related_name='%(app_label)s_%(class)s_uploaded_by')

    class Meta:
        verbose_name = {{ cookiecutter.model_name }}
        verbose_name_plural = {{ cookiecutter.model_name_plural }}
        # replaces <modelname>_set to model_name
        related_name = {{ cookiecutter.model_name_plural }}
    #     permissions = [
    #         ('add_{{cookiecutter.model_name}}_<model_fk>', 'Can add {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #         ('change_{{cookiecutter.model_name}}_<model_fk>', 'Can change {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #         ('view_{{cookiecutter.model_name}}_<model_fk>', 'Can view {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #         ('remove_{{cookiecutter.model_name}}_<model_fk>', 'Can remove {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #         ('delete_{{cookiecutter.model_name}}_<model_fk>', 'Can delete {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #     ]

    def __str__(self):
        return self.name

    @classmethod
    def get_create_url(self):
        return reverse(
            "{{cookiecutter.model_name}}:create", 
            kwargs={"pk": self.pk}
            )

    def get_absolute_url(self):
        return reverse(
            "{{cookiecutter.model_name}}:detail", 
            kwargs={"pk": self.pk}
            )

    def get_update_url(self):
        return reverse(
            "{{cookiecutter.model_name}}:update", 
            kwargs={"pk": self.pk}
            )

    def get_delete_url(self):
        return reverse(
            "{{cookiecutter.model_name}}:delete", 
            kwargs={"pk": self.pk}
            )
