from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from utils.lambdas import confidential_upload
from utils.base_models.fields import InternalFileField
from utils.base_models.models import AbstractAuditedModel
from utils.file_encryptor import AccessClassification

# Create your models here.
class DocumentMetadata(AbstractAuditedModel):
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
    access_classification = models.IntegerField(verbose_name="Access Classification", choices=AccessClassification.choices)
    def __str__(self):
        return self.name

# Create your models here.
class DocumentSubmission(AbstractAuditedModel):
    metadata = models.ForeignKey(DocumentMetadata, on_delete=models.RESTRICT, verbose_name="File Submission Type")
    attachment = InternalFileField(upload_to=confidential_upload)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, blank=False)
    notes = models.TextField(verbose_name="Extra information about document submitted", null=True, blank=True)

    def __str__(self):
        return f"{self.metadata} - {self.content_object}"

    def get_absolute_url(self):
        return f'{reverse("file:pdf")}?file={self.attachment.url}'

    def get_tokenized_absolute_url_for_user(self, user):
        return f'{reverse("file:pdf")}?file={self.attachment.url}&token={self.first_object_token_chars}{user.object_token}'

    class Meta:
        ordering = ["-modified_at"]