from auditlog.models import AuditlogHistoryField
from auxiliaries.status_tags.models import StatusTag
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
import os

def rename_upload(instance, filename):
    filename, ext = os.path.splitext(filename)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f"{slugify(instance.name)}_{instance.updated_by}_{timestamp}{ext}" 

# Create your models here.
class DocumentMetadata(models.Model):
    name = models.CharField(
        max_length=240,
        blank=True,
        null=True,
    )
    description = models.TextField(
        default='',
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_updated_by')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    require_for_tags = models.ManyToManyField(
        StatusTag,
        blank=True,
        )

    def __str__(self):
        return self.name

# Create your models here.
class DocumentSubmission(models.Model):
    metadata = models.ForeignKey(DocumentMetadata, on_delete=models.RESTRICT)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_updated_by')
    attachment = models.FileField(upload_to=rename_upload)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    history = AuditlogHistoryField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'{reverse("file:pdf")}?file={self.attachment}'