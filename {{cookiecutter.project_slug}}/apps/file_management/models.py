from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.text import slugify
from utils import lambdas
from utils.lambdas import YN_BOOLEAN_CHOICES
from utils.base_models.models import AbstractAuditedModel

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
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    is_downloadable = models.BooleanField(
        verbose_name="Can document be downloaded?", default=True,
        choices=YN_BOOLEAN_CHOICES,
    )

    def __str__(self):
        return self.name

# Create your models here.
class DocumentSubmission(AbstractAuditedModel):
    metadata = models.ForeignKey(DocumentMetadata, on_delete=models.RESTRICT)
    attachment = models.FileField(upload_to=lambdas.rename_upload)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.name

    @property
    def is_downloadable(self):
        return self.metadata.is_downloadable

    @property
    def as_embedded_html_element(self):
        return render_to_string('detail_wrapper/pdf.html', context={'object':self})

    def get_absolute_url(self):
        return f'{reverse("file:pdf")}?file={self.attachment}'