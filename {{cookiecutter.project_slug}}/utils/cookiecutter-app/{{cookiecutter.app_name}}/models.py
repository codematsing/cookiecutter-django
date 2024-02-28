from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from utils import lambdas
from utils.base_models.models import AbstractAuditedModel, BaseModelMixin
from utils.base_models import fields
from django.template.loaders import render_to_string
import os

# Create your models here.
class {{cookiecutter.model_name_camel_case}}Manager(models.Manager):
    pass

class {{cookiecutter.model_name_camel_case}}(BaseModelMixin, AbstractAuditedModel):
    objects = {{cookiecutter.model_name_camel_case}}Manager()

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
    description = fields.RichTextareaFormField()
    date = fields.DateField(auto_now=True)
    datetime = fields.DateTimeField(auto_now=True)
    image = fields.ImageField()
    attachment = fields.FileField(upload_to=lambdas.rename_upload)
    fk_model = fields.ForeignKey(on_delete=models.CASCADE)
    o2o_model = fields.OneToOne(on_delete=models.CASCADE)
    m2m_model = fields.ManyToManyField()
    int_choice = fields.IntegerChoiceField(choices=[])
    text_choice = fields.TextChoiceField(choices=[])
    is_boolean = models.BooleanField(default=False, choices=[(True, "True"), (False, "False")])
    is_nullable_boolean = models.BooleanField(null=True, blank=True, choices=[(None, "Pending"), (True, "True"), (False, "False")])

    class Meta:
        # https://docs.djangoproject.com/en/4.2/ref/models/options/
        db_table_comment = "{{ db_table_comment }}"
        verbose_name = "{{ model_name_verbose_name}}"
        verbose_name_plural = "{{ model_name_verbose_name_plural }}"
        app_label = "{{ cookiecutter.app_name_snake_case_plural }}"
        default_related_name = "{{ cookiecutter.app_name_snake_case_plural }}"
        # ordering = []
        # get_latest_by = []
        # unique_together = []
    #     permissions = [
    #         ('add_{{cookiecutter.model_name}}_<model_fk>', 'Can add {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #         ('change_{{cookiecutter.model_name}}_<model_fk>', 'Can change {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #         ('view_{{cookiecutter.model_name}}_<model_fk>', 'Can view {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #         ('remove_{{cookiecutter.model_name}}_<model_fk>', 'Can remove {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #         ('delete_{{cookiecutter.model_name}}_<model_fk>', 'Can delete {{ cookiecutter.model_name[:-1]|replace('_', ' ')|title}} <model_fk>'),
    #     ]

    # ensure to override if needed. See BaseModelMixin for default url methods:
    # * get_list_url
    # * get_create_url
    # * get_absolute_url
    # * get_update_url
    # * get_delete_url
    # * add additional urls related to model if needed. see urls.py