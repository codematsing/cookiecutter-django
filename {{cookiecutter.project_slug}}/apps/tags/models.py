from django.db import models
from colorfield.fields import ColorField
from django.template.loader import render_to_string

# Create your models here.

class BaseTag(models.Model):
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
    foreground = ColorField(default="#000000")
    background = ColorField(default="#FFFFFF")

    @property
    def as_html(self):
        return render_to_string('detail_wrapper/badge.html', context={'field':self})

    class Meta:
        app_label = "tags"

    def __str__(self):
        return self.name
