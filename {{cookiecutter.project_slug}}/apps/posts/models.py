from django.db import models
from django.urls import reverse
from django.template.loader import render_to_string
from utils import lambdas
from utils.base_models.models import AbstractAuditedModel
from utils.base_models import fields

import os

# Create your models here.
class Post(AbstractAuditedModel):
    title = models.CharField(
        max_length=240,
        unique=True
    )
    body = models.TextField(null=True, blank=True)
    thumbnail = fields.ImageField(upload_to=lambdas.image_upload, blank=True, null=True)
    is_published = fields.BooleanField(
        default=False, 
        verbose_name="Publish post", 
        )

    def __str__(self):
        return str(self.title)

    @property
    def is_drafted(self):
        return not self.is_published

    @property
    def is_published_as_badge(self):
        field_item = {
            'name': "Published" if self.is_published else "Drafted",
            'background': "#184425" if self.is_published else "#a0a0a0",
            'foreground': "#FFFFFF" if self.is_published else "#FFFFFF",
        }
        return render_to_string('detail_wrapper/badge.html', {'field':field_item})

    def get_absolute_url(self):
        return reverse(
            "posts:detail",
            kwargs={"pk": self.pk}
            )

    def get_update_url(self):
        return reverse(
            "posts:update",
            kwargs={"pk": self.pk}
            )

    def get_delete_url(self):
        return reverse(
            "posts:delete",
            kwargs={"pk": self.pk}
            )

    class Meta:
        ordering = ['-history__timestamp', 'is_published']
        get_latest_by = 'history__timestamp'