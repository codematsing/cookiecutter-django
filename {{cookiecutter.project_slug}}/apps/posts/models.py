from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from utils import lambdas
from utils.base_models.models import AbstractAuditedModel

import os

# Create your models here.
class Post(AbstractAuditedModel):
    title = models.CharField(
        max_length=240,
        unique=True
    )
    body = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to=lambdas.image_upload, blank=True, null=True)
    is_published = models.BooleanField(
        default=False, 
        verbose_name="Publish post", 
        choices=((False, 'Save as draft'), (True, 'Publish Post'))
        )

    def __str__(self):
        return str(self.title)

    @property
    def is_drafted(self):
        return not self.is_published

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