from django.urls import reverse
from auditlog.models import AuditlogHistoryField
from utils.lambdas import get_current_domain
from utils.detail_wrapper.mixins import DetailCard
from softdelete.models import SoftDeleteObject, SoftDeleteManager
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db import models
import logging
import uuid
import re
logger = logging.getLogger(__name__)

# Create your models here.
class BaseModelManager(SoftDeleteManager):
	pass

class AbstractBaseModel(SoftDeleteObject):
	# please note to always inherit BaseModelManager
	objects = BaseModelManager()

	@classmethod
	def get_contentype_for_model(cls):
		return ContentType.objects.get_for_model(cls)

	@property
	def db_identifier(self):
		return f"{self.get_contentype_for_model().pk}-{self.pk}"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not isinstance(self.__class__.objects, SoftDeleteManager):
			raise ValueError(f"{self.__class__}.objects must inherit utils.base_models.models.BaseModelManager")

	def field_dict(self):
		return {field.name:getattr(self, field.name) for field in self._meta.fields}


	@property
	def as_anchor_tag(self):
		return f"<a href='{self.get_absolute_url()}'>{self}</a>"

	def as_card(self, fields='__all__', **kwargs):
		return DetailCard(self, fields=fields, **kwargs).card

	@property
	def as_href(self):
		return f"<a href='{self.get_full_absolute_url()}'>{self}<a/>"

	@classmethod
	def get_list_url(cls):
		return reverse(
			f"{cls._meta.app_label}:list",
			)

	@classmethod
	def get_ajax_list_url(cls):
		return reverse(
			f"{cls._meta.app_label}:ajax:list",
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
	def get_full_list_url(cls):
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
		if hasattr(self, 'name'):
			return self.name
		return f"{self._meta.verbose_name} {self.pk}"

	class Meta:
		abstract = True

class AbstractAuditedModel(AbstractBaseModel):
	history = AuditlogHistoryField()
	modified_at = models.DateTimeField(verbose_name="Log Entry Added", editable=False, auto_now=False, auto_now_add=False, null=True, blank=True)
	object_token = models.UUIDField(null=False, blank=False, editable=False, default=uuid.uuid4)
	_additional_data = None

	@property
	def first_object_token_chars(self):
		return re.findall(r'\w+', str(self.object_token))[0]

	@property
	def last_object_token_chars(self):
		return re.findall(r'\w+', str(self.object_token))[-1]

	def get_access_token_for_user(self, user):
		return f"{self.last_object_token_chars}{user.last_object_token_chars}"

	def save(self, *args, **kwargs):
		if self._additional_data:
			self.modified_at = timezone.now()
		return super().save(*args, **kwargs)

	def get_additional_data(self):
		return self._additional_data

	@property
	def updated_by(self):
		try:
			return getattr(self.history.latest(), 'actor', None)
		except Exception as e:
			return None

	@property
	def updated_at(self):
		return self.history.latest().timestamp

	@property
	def created_at(self):
		return self.history.earliest().timestamp

	@property
	def latest_additional_data(self):
		return getattr(self.history.latest(), 'additional_data', None)

	@classmethod
	def get_history_column_defs(self):
		return [
			{'name':'pk', 'visible':False},
			{'name':'timestamp', 'searchable':False},
			{'name':'actor', 'title':'Updated by', 'foreign_field':'actor__username'},
			{'name':'action', 'title':'Action done'},
			{'name':'changes', 'title':'Changes', 'searchable':False},
			{'name':'additional_data', 'title':'Remarks'},
		]

	@classmethod
	def get_history_customize_row(self, row, obj):
		row["changes"] = "<br/>".join(str(field) for field in obj.changes_display_dict.keys())
		row["additional_data"] = render_to_string(
			'history_management/additional_data.html', 
			context={'additional_data':obj.additional_data}
			)

	class Meta:
		abstract=True