from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from logging import getLogger
from django.urls import reverse
from django.contrib.auth.models import Group
from utils.base_models.models import BaseModelMixin

logger = getLogger(__name__)

class SidebarClassification(models.IntegerChoices):
    INTERNAl = 1
    CONFIDENTIAL = 2

# Create your models here.
class SidebarItem(BaseModelMixin, models.Model):
    header = models.CharField(max_length=32, verbose_name="Sidebar grouping header", default="HOME", validators=[RegexValidator(r"[A-Z\ ]+", message="Must be capitalized")])
    label = models.CharField(max_length=32, null=False, blank=False, unique=True)
    description = models.CharField(max_length=128, null=True, blank=True, verbose_name="Description", help_text="short description about module")
    href = models.CharField(max_length=64, null=False, blank=False, verbose_name="Entry point href to module", unique=True)
    icon = models.CharField(max_length=64, default="mdi-play", verbose_name="Material Design Icon Code", help_text="ex. mdi-power", validators=[RegexValidator(r'[a-z\-]+', message="Must be one word, dash-separated")])
    classification = models.IntegerField(choices=SidebarClassification.choices, default=SidebarClassification.INTERNAl, help_text="Show to: Public - Anyone, Internal - Logged in, Confidential - Only allowed roles / groups")
    priority_number = models.IntegerField(verbose_name="Priority Order in sidebar (1 being top-most)", default=5)
    groups = models.ManyToManyField(Group, blank=True, related_name="sidebar_items")

    @property
    def as_nav_link(self):
        return render_to_string("partials/admin/sidebar/nav_link.html", context={'object':self})
        
    def save(self, *args, **kwargs):
        if not self.href:
            self.href = self.content_type.model_class().get_list_url()
            logger.debug(f"No url found. Will be prefilled to: {self.href}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("modules:detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("modules:update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("modules:delete", kwargs={"pk": self.pk})

    @classmethod
    def get_create_url(cls):
        return reverse("modules:create", kwargs={})

    def __str__(self):
        return self.label

    class Meta:
        app_label="module_management"
        verbose_name = "Sidebar Item"
        verbose_name_plural = "Sidebar Items"
        ordering = ["header", "priority_number", "label"]
