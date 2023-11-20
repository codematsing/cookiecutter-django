from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from auditlog.models import AuditlogHistoryField

# Create your models here.
class AbstractAuditedModel(models.Model):
    comments = models.TextField(null=True, blank=True, help_text="Provide supporting notes to your submission for both student and officers to see")
    history_remarks = models.CharField(
        max_length=1024, 
        verbose_name="Diary log or reason for changes in record",
        blank=True, 
        null=True
    )
    history = AuditlogHistoryField()

    def render_status(self):
        if self.status:
            return self.status
        else:
            return 'Unknown Status'
    
    class Meta:
        abstract=True