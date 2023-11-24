from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from auditlog.models import AuditlogHistoryField
from django.template.loader import render_to_string

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

class BaseModel(models.Model):
    detail_card_template = None

    def field_dict(self):
        return {field.name:getattr(self, field.name) for field in self._meta.fields}

    def _init_fields_as_html(self):
        for field in self._meta.fields:
            field_name_as_html = f"{field.name}_as_html"
            if not hasattr(self, field_name_as_html):
                # TODO: refer to detail_wrappper for default rules
               setattr(self, field_name_as_html, field.attr)
            else, will leave empty to call custom field property

    def __init__(self):
        super().__init__
        self._init_fields_as_html()

    @property
    def as_html(self):
        return f"<a href='{self.get_absolute_url()}'>{self}</a>"

    def as_card(self, fields='__all__'):
        return render_to_string('detail_wrapper/detail_card.html', self)

    def _render_breadcrumbs_as_html(self, breadcrumbs):
        return render_to_string('partials/common/breadcrumbs.html')

    # breadcrumbs
    @classmethod
    def get_list_breadcrumbs(self, as_html=False):
        breadcrumbs = {
            self._meta.verbose_name_plural : self.get_list_url()
        }
        if as_html:
            return self._render_breadcrumbs_as_html(breadcrumbs)
        return breadcrumbs

    @classmethod
    def get_create_breadcrumbs(self, as_html=False):
        breadcrumbs = self.get_list_breadcrumbs()
        breadcrumbs.update({'Create':self.get_list_url()})
        if as_html:
            return self._render_breadcrumbs_as_html(breadcrumbs)
        return breadcrumbs

    def get_detail_breadcrumbs(self, as_html=False):
        breadcrumbs = self.get_list_breadcrumbs()
        breadcrumbs.update({
            self : self.get_absolute_url(),
        })
        if as_html:
            return self._render_breadcrumbs_as_html(breadcrumbs)
        return breadcrumbs

    def get_update_breadcrumbs(self, as_html=False):
        breadcrumbs = self.get_list_breadcrumbs()
        breadcrumbs.update({
            self : self.get_absolute_url(),
        })
        if as_html:
            return self._render_breadcrumbs_as_html(breadcrumbs)
        return breadcrumbs

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
