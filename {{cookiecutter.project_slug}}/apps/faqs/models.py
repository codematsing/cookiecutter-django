from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from utils.base_models.models import AbstractAuditedModel
import os

# def rename_upload(instance, filename):
#     filename, ext = os.path.splitext(filename)
#     timestamp = instance.updated_at.strftime('%Y%m%d%H%M%S')
#     return f"{instance.name}_v{instance.version_no}_{timestamp}{ext}" 

# Create your models here.
class FaqItem(AbstractAuditedModel):
    question = models.CharField(
        max_length=1024, 
        blank=False, 
        null=False
    )
    answer = models.TextField(null=False, blank=False)
    order = models.IntegerField(default=5)
    is_published = models.BooleanField(default=False, verbose_name="Publish FAQ", choices=((False, 'Save as draft'), (True, 'Publish FAQ')))

    class Meta:
        ordering = ["order"]

    @property
    def is_drafted(self):
        return not self.is_published


    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse(
            "managed_faqs:detail", 
            kwargs={"pk": self.pk}
            )

    def get_update_url(self):
        return reverse(
            "managed_faqs:update", 
            kwargs={"pk": self.pk}
            )

    def get_delete_url(self):
        return reverse(
            "managed_faqs:delete", 
            kwargs={"pk": self.pk}
            )

    def as_card(self):
        return render_to_string('faqs/as_card.html', {'object':self})