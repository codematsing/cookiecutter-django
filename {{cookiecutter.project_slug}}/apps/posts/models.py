from django.db import models
from django.urls import reverse
from django.template.loader import render_to_string
from utils import lambdas
from utils.base_models.models import AbstractAuditedModel
from utils.base_models import fields
from django.utils import timezone
from dateutil import relativedelta
from tags.models import BaseTag
import logging
logger = logging.getLogger(__name__)


# Create your models here.
class PostTag(BaseTag):
    pass
class Post(AbstractAuditedModel):
    title = models.CharField(
        max_length=240,
        unique=True
    )
    body = models.TextField(null=True, blank=True)
    thumbnail = fields.ImageField(upload_to=lambdas.public_upload, blank=True, null=True)
    is_published = models.BooleanField(
        default=False, 
        verbose_name="Publish post?",
        choices=[[True, "Publish"], [False, "Save As Draft"]]
        )
    tags = models.ManyToManyField(PostTag, related_name="posts")

    def __str__(self):
        return str(self.title)

    @property
    def is_drafted(self):
        return not self.is_published

    @property
    def is_3_days_recent(self):
        return relativedelta.relativedelta(timezone.now(), self.updated_at).days<=3

    @property
    def is_published_as_badge(self):
        field_item = {
            'name': "Published" if self.is_published else "Drafted",
            'background': "#184425" if self.is_published else "#a0a0a0",
            'foreground': "#FFFFFF" if self.is_published else "#FFFFFF",
        }
        return render_to_string('detail_wrapper/badge.html', {'field':field_item})

    @classmethod
    def get_list_url(cls):
        return reverse(
            f"posts_management:list",
            )

    def get_absolute_url(self):
        return reverse(
            "post_detail",
            kwargs={"pk": self.pk}
            )

    def get_update_url(self):
        return reverse(
            f"posts_management:update",
            kwargs={"pk": self.pk}
            )

    def get_delete_url(self):
        return reverse(
            f"posts_management:update",
            kwargs={"pk": self.pk}
            )

    class Meta:
        ordering = ['-history__timestamp', 'is_published']
        get_latest_by = 'history__timestamp'