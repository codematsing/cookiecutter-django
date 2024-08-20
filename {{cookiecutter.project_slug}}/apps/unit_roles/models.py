from django.db import models
from utils.base_models.models import AbstractAuditedModel, BaseModelManager
from role_management.models import Role
from units.models import Unit
from utils.detail_wrapper.mixins import DetailCard

# Create your models here.
class UnitRoleManager(BaseModelManager):
    pass

class UnitRole(AbstractAuditedModel):
    objects = UnitRoleManager()

    role = models.ForeignKey(Role, verbose_name="Role", on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, verbose_name="Unit", on_delete=models.CASCADE)
    class Meta:
        # https://docs.djangoproject.com/en/4.2/ref/models/options/
        db_table_comment = "Brief description about unit_roles"
        verbose_name = "Unit Role"
        verbose_name_plural = "Unit Roles"
        app_label = "unit_roles"
        default_related_name = "unit_roles"

    def __str__(self):
        return f"{self.unit} {self.role}"

    @property
    def as_table_row(self):
        return DetailCard(
            self, 
            template="pages/admin/profile/unit_role.html",
            fields=[
                "unit", "role"
            ]
        ).template_html
