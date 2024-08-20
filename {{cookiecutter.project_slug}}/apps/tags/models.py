from django.db import models
from django.template.loader import render_to_string
from django.core.validators import RegexValidator
from utils.base_models.models import AbstractAuditedModel

# Create your models here.

class BaseTag(AbstractAuditedModel):
    name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        unique=True
    )

    description = models.TextField(
        max_length=1024,
        null=True,
        blank=True,
    )
    foreground = models.CharField(default="#000000", validators=[RegexValidator(regex=r"#\d{6}")])
    background = models.CharField(default="#FFFFFF", validators=[RegexValidator(regex=r"#\d{6}")])
    requires_log_entry_on_update = models.BooleanField(default=False, help_text="System identifier if feedback is required for status change")

    @property
    def as_html(self):
        return render_to_string('detail_wrapper/badge.html', context={'field':self})

    class Meta:
        app_label = "tags"

    def __str__(self):
        return self.name
