from django.db import models
from django.urls import reverse
from auditlog.models import AuditlogHistoryField
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from utils.lambdas import get_current_domain
from utils.detail_wrapper.mixins import DetailCard
import pandas as pd

# Create your models here.
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

class BaseModelMixin:
    def field_dict(self):
        return {field.name:getattr(self, field.name) for field in self._meta.fields}

    @property
    def as_anchor_tag(self):
        return f"<a href='{self.get_absolute_url()}'>{self}</a>"

    @property
    def as_card(self):
        return DetailCard(self).card

    @classmethod
    def get_list_url(cls):
        return reverse(
            f"{cls._meta.app_label}:list",
            )

    @classmethod
    def get_create_url(cls):
        return reverse(
            f"{cls._meta.app_label}:create",
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
            f"{self._meta.app_label}:delete",
            kwargs={"pk": self.pk}
            )

    @classmethod
    def get_list_url(cls):
        return f"{get_current_domain()}{cls.get_list_url()}"

    @classmethod
    def get_full_create_url(cls):
        return f"{get_current_domain()}{cls.get_create_url()}"

    def get_full_absolute_url(self):
        return f"{get_current_domain()}{self.get_absolute_url()}"

    def get_full_update_url(self):
        return f"{get_current_domain()}{self.get_update_url()}"

    def get_full_delete_url(self):
        return f"{get_current_domain()}{self.get_delete_url()}"

    def __str__(self):
        return self.name

class AbstractAuditedModel(BaseModelMixin, HistoryMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_verified_by')
    history = AuditlogHistoryField()

    def render_status(self):
        if self.status:
            return self.status
        else:
            return 'Unknown Status'
    
    class Meta:
        abstract=True