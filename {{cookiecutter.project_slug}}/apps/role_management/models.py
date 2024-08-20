from django.db import models
from utils.base_models.models import AbstractAuditedModel, BaseModelManager
from utils.base_models import fields
from django.contrib.auth.models import Group
from django.urls import reverse
import os

# Create your models here.
class RoleManager(BaseModelManager):
    pass

class Role(AbstractAuditedModel, Group):
    objects = RoleManager()

    class Meta:
        # https://docs.djangoproject.com/en/4.2/ref/models/options/
        db_table_comment = "Brief description about role_management"
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        app_label = "role_management"
        default_related_name = "role_management"
        # ordering = []
        # get_latest_by = []
        # unique_together = []
    #     permissions = [
    #         ('add_role_<model_fk>', 'Can add Role <model_fk>'),
    #         ('change_role_<model_fk>', 'Can change Role <model_fk>'),
    #         ('view_role_<model_fk>', 'Can view Role <model_fk>'),
    #         ('remove_role_<model_fk>', 'Can remove Role <model_fk>'),
    #         ('delete_role_<model_fk>', 'Can delete Role <model_fk>'),
    #     ]

    # ensure to override if needed. See BaseModelMixin for default url methods:
    # * get_list_url
    # * get_create_url
    # * get_absolute_url
    # * get_update_url
    # * get_delete_url
    # * add additional urls related to model if needed. see urls.py

    def get_absolute_url(self):
        return reverse("role_management:detail", kwargs={"pk": self.pk})
    
    def get_update_url(self):
        return reverse("role_management:update", kwargs={"pk": self.pk})
    