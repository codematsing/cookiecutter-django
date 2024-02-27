from django.db import models
from django.urls import reverse
from auditlog.models import AuditlogHistoryField
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from utils.detail_wrapper.mixins import DetailCard
import pandas as pd

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

class HistoryMixin:
    def get_history_df(self, columns = ["updated_by", "status", "comments"]):
        history_df = pd.DataFrame()
        for entry in self.history.all():
            record = entry.changes_dict
            _items = {'updated_at':entry.timestamp}
            for key in ['updated_by', 'status', 'comments']:
                record.get(key, [None, None])
            _items.update({key:record.get(key, [None,None])[1] for key in columns})
            history_df =history_df.append(_items, ignore_index=True)
        history_df['updated_at'] = history_df['updated_at'].dt.tz_convert("Asia/Manila").dt.strftime("%Y-%m-%d %I:%M %p")
        history_df.dropna(thresh=2, inplace=True)
        history_df.fillna("None", inplace=True)
        history_df.columns = pd.Series(history_df.columns).apply(lambda col: f"<b>{col.replace('_', ' ').capitalize()}</b>")
        return history_df

    @property
    def history_as_table(self):
        history_table = self.get_history_df().to_html(index=False, render_links=True, classes="table table-striped", justify="left", escape=False)
        return render_to_string('partials/common/history.html', {'object':self, 'history_table':history_table})

class BaseModel(models.Model):
    def field_dict(self):
        return {field.name:getattr(self, field.name) for field in self._meta.fields}

    @property
    def as_anchor_tag(self):
        return f"<a href='{self.get_absolute_url()}'>{self}</a>"

    def as_card(self, fields='__all__'):
        return DetailCard(self, fields)

    @classmethod
    def get_list_url(self):
        return reverse(
            f"{self._meta.app_label}:list",
            )

    @classmethod
    def get_create_url(self):
        return reverse(
            f"{self._meta.app_label}:create",
            )

    def get_absolute_url(self):
        return reverse(
            f"{self._meta.app_label}:detail",
            kwargs={"pk": self.pk}
        )

    def get_update_url(self):
        return reverse(
            f"{self._meta.app_label}:update",
            kwargs={"pk": self.pk}
            )

    def get_delete_url(self):
        return reverse(
            "{{cookiecutter.app_name}}:delete", 
            kwargs={"pk": self.pk}
            )

    def __str__(self):
        return self.name

class AbstractTrackedSubmission(HistoryMixin, BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_verified_by')
    comments = models.TextField(null=True, blank=True, verbose_name="Submission Notes", help_text="Provide supporting notes to your submission for both student and officers to see")
    history = AuditlogHistoryField()

    def render_status(self):
        if self.status:
            return self.status
        else:
            return 'Unknown Status'
    
    @property
    def history_as_table(self):
        return render_to_string('partials/common/history.html', {'history_list':self.get_history_df()})

    class Meta:
        abstract=True
        app_label="auxiliaries"

class AbstractTrackedRecord(HistoryMixin, BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_updated_by')
    comments = models.TextField(null=True, blank=True, verbose_name="Submission Notes", help_text="Provide supporting notes to your submission for officers, applicants, and scholars to see")
    history = AuditlogHistoryField()
    class Meta:
        abstract=True
        app_label="auxiliaries"