from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from utils import lambdas
from utils.base_models.models import AbstractAuditedModel, BaseModel
from utils.base_models import fields
from django.template.loaders import render_to_string
import os

# Create your models here.
class {{cookiecutter.camel_case_model_name}}Manager(models.Manager):
    pass

class {{cookiecutter.camel_case_model_name}}(AbstractAuditedModel, BaseModel):
    objects = {{cookiecutter.camel_case_model_name}}Manager()

    name = models.CharField(
        max_length=128, 
        blank=True, 
        null=True,
        default=None,
        verbose_name=None,
        help_text=None,
        validators=None,
        choices=None,
        unique=None,
    )
    # date = fields.DateField(upload_to=lambdas.rename_upload)
    # description = fields.RichTextareaFormField()
    # image = fields..ImageField()
    # attachment = fields.FileField(upload_to=lambdas.rename_upload)
    # uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT, related_name='%(app_label)s_%(class)s_uploaded_by')

    class Meta:
        verbose_name = "{{ cookiecutter.model_name }}"
        verbose_name_plural = "{{ cookiecutter.model_name_plural }}"
        # replaces <modelname>_set to model_name
        app_label = "{{ cookiecutter.app_name }}"
        related_name = "{{ cookiecutter.model_name_plural }}"
        ordering = []
        get_latest_by = []
        unique_together = []
    #     permissions = [
    #         ('add_{{cookiecutter.model_name}}_<model_fk>', 'Can add {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #         ('change_{{cookiecutter.model_name}}_<model_fk>', 'Can change {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #         ('view_{{cookiecutter.model_name}}_<model_fk>', 'Can view {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #         ('remove_{{cookiecutter.model_name}}_<model_fk>', 'Can remove {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #         ('delete_{{cookiecutter.model_name}}_<model_fk>', 'Can delete {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #     ]

    # ensure to override if needed. See BaseModel for default url methods:
    # * get_list_url
    # * get_create_url
    # * get_absolute_url
    # * get_update_url
    # * get_delete_url
    # * add additional urls related to model if needed. see urls.py