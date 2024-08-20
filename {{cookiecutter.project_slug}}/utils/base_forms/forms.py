from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput
from formset.richtext.widgets import RichTextarea
from formset.collection import FormCollection
from formset.fieldset import FieldsetMixin, Fieldset
from formset.renderers.bootstrap import FormRenderer
from formset.widgets import Selectize, SelectizeMultiple, DualSelector, UploadedFileInput
from utils.validators import EmailValidator
from auxiliaries.status_tags.form_status.models import FormStatus
import logging
logger = logging.getLogger(__name__)



class PdfFileWidget(UploadedFileInput):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.attrs.update({
			"max-size": 1024 * 1024 * 10,  # 10mb
			"accept": 'application/pdf',
		})

class ImageFileWidget(UploadedFileInput):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.attrs.update({
			"max-size": 1024 * 1024 * 1,  # 1
			"accept": 'image/png, image/jpeg',
		})

class ExtraNotesForm(Fieldset):
	legend = "Extra Notes"
	notes = forms.CharField(label="Extra Notes", max_length=2048, widget=RichTextarea(), required=False, help_text="Extra information you may want to communicate with Student Affairs Officers")
	require_on_update = True

	def __init__(self, *args, **kwargs):
		self.require_on_update = kwargs.pop('require_on_update', True)
		return super().__init__(*args, **kwargs)

	def clean_notes(self):
		if getattr(self, "instance", None) and not self.cleaned_data["notes"] and self.require_on_update:
			raise ValidationError("Requires extra notes for updating of profile")
		return self.cleaned_data['notes']

class LogEntryForm(Fieldset):
	legend = "Log Entry" 

	log_entry = forms.CharField(
			label="Log Entry", 
			help_text="Provide log remarks related to purpose of update", 
			required=False, 
			max_length=2048, 
			widget=RichTextarea()
		)

	def clean_log_entry(self):
		if getattr(self, "instance", None) and not self.cleaned_data["log_entry"]:
			raise ValidationError("Requires reason for change")
		return self.cleaned_data['log_entry']

class CustomSelectize(Selectize):
	max_prefetch_choices = 700
	# customize due to cap of original

	@staticmethod
	def _choice_has_empty_value(choice):
		"""Return True if the choice's value is empty string or None."""
		# Weird bug: too many values to unpack (expected 2)
		value = None
		if len(choice)==3:
			_, value, _ = choice
		else:
			value, _ = choice
		return value is None or value == ""

class CustomSelectizeMultiple(SelectizeMultiple):
	max_prefetch_choices = 700
	# customize due to cap of original

class CustomDualSelector(DualSelector):
	max_prefetch_choices = 700
	# customize due to cap of original

class MultiEmailField(forms.Field):

	def to_python(self, value):
		"""Normalize data to a list of strings."""
		# Return an empty list if no input was given.
		# remove any spaces and lines
		value = value.replace(" ", "").replace("\n", "") if value else []
		return value.split(",")

	def validate(self, value):
		"""Check if value consists only of valid emails."""
		# Use the parent's handling of required fields, etc.
		for email in value:
			EmailValidator()(email)

class BaseForm(Fieldset):
	default_renderer = FormRenderer

	def __init__(self, *args, **kwargs):
		self.extra_data = kwargs.pop('extra_data', {})
		self.request = self.extra_data.get('request', None)
		self.instance = kwargs.pop('instance', {})
		super().__init__(*args, **kwargs)

class DeleteForm(BaseForm):
	copy_object_str = forms.CharField(
		label="Copy Key", 
		max_length=256, 
		disabled=True, 
		help_text="Please copy key to succeeding field to delete"
	)
	object_str = forms.CharField(label="Delete Key", max_length=256)

	def __init__(self, *args, **kwargs):
		self.instance = kwargs.pop('instance')
		self.extra_data = kwargs.pop('extra_data')
		super().__init__(*args, **kwargs)
	
	def clean(self):
		logger.info(self.cleaned_data)
		logger.info(self.instance)
		if self.cleaned_data["object_str"]!=self.cleaned_data["copy_object_str"]:
			raise ValidationError("Invalid Key")
		return self.cleaned_data

class BaseModelForm(FieldsetMixin, forms.ModelForm):
	default_renderer = FormRenderer

	def set_meta_fields(self):
		fields = set(getattr(self.Meta, 'fields', []))
		if fields != '__all__':
			fields = (fields.union(self.disabled_fields).union(self.hidden_fields))

	def set_hidden_fields(self, kwargs):
		self.hidden_fields = set(getattr(self.Meta, 'hidden_fields', []))
		if 'hidden_fields' in kwargs:
			self.hidden_fields = self.hidden_fields.union(set(kwargs['hidden_fields']))

	def set_disabled_fields(self, kwargs):
		self.disabled_fields = set(getattr(self.Meta, 'disabled_fields', []))
		if 'disabled_fields' in kwargs:
			self.disabled_fields = self.disabled_fields.union(set(kwargs['disabled_fields']))

	def disable_fields(self, fields):
		for elem in fields:
			self.fields[elem].disabled = True

	def hide_fields(self, fields):
		for elem in fields:
			self.disable_fields([elem])
			self.fields[elem].widget = HiddenInput()

	def __init__(self, *args, **kwargs):
		self.extra_data = kwargs.pop('extra_data', {})
		self.request = self.extra_data.get('request', None)
		self.set_disabled_fields(kwargs)
		self.set_hidden_fields(kwargs)
		self.set_meta_fields()
		super().__init__(*args, **kwargs)
		self.disable_fields(self.disabled_fields)
		self.hide_fields(self.hidden_fields)

class BaseFormCollection(FormCollection):
	default_renderer = FormRenderer
	extra_data = {}
	object_data = {}

	def __init__(self, **kwargs):
		self.extra_data = kwargs.pop('extra_data', {})
		self.request = self.extra_data.get('request', None)
		super().__init__(**kwargs)
		#https://github.com/jrief/django-formset/issues/159
		if self.instance:
			self.object_data = {k:v for k,v in vars(self.instance).items() if not k.startswith('_')}

	#https://github.com/jrief/django-formset/issues/159
	def full_clean(self):
		super().full_clean()
		# note that if self.cleaned_data is not working, then there are current errors in form
		# if not getattr(self, 'cleaned_data', None):
		# 	logger.warning(f"""
		# 		Cannot get cleaned data due to error
		# 	""")
		# 	logger.warning(self._errors)
		if self.instance:
			for key, value in self.object_data.items():
				setattr(self.instance, key, value)

	def set_meta_fields(self):
		fields = set(getattr(self.Meta, 'fields', []))
		if fields != '__all__':
			fields = (fields.union(self.disabled_fields).union(self.hidden_fields))

	def set_hidden_fields(self, kwargs):
		self.hidden_fields = set(getattr(self.Meta, 'hidden_fields', []))
		if 'hidden_fields' in kwargs:
			self.hidden_fields = self.hidden_fields.union(set(kwargs['hidden_fields']))

	def set_disabled_fields(self, kwargs):
		self.disabled_fields = set(getattr(self.Meta, 'disabled_fields', []))
		if 'disabled_fields' in kwargs:
			self.disabled_fields = self.disabled_fields.union(set(kwargs['disabled_fields']))

	def disable_fields(self, fields):
		for elem in fields:
			self.fields[elem].disabled = True

	def hide_fields(self, fields):
		for elem in fields:
			self.disable_fields([elem])
			self.fields[elem].widget = HiddenInput()

	def save(self):
		raise NotImplementedError("Need to provide saving mechanism for Form")

	def create(self):
		return self.save()

	def update(self):
		return self.save()

		
	#TODO: form collection hidden and disabled fields

class FormVerificationForm(BaseForm):
	"""
		A generic form for verification of models. Accepts an object instance.
		Reason for being generic is to accomodate all models that inherits AbstractTrackedSubmission
	"""
	status = forms.ModelChoiceField(queryset=FormStatus.objects.verification_options(), required=True)
	feedback = forms.CharField(label="Feedback", max_length=2048, widget=RichTextarea)

	def clean(self):
		logger.info(self.instance)
		cleaned_data = super().clean()
		logger.info(cleaned_data)
		if cleaned_data['status'] in FormStatus.objects.required_supplmentary_feedback_statuses() and not cleaned_data['feedback']:
			self.add_error("feedback", "Requires reason pending status")
		return cleaned_data

	def save(self, commit=True):
		feedback = self.cleaned_data["feedback"]
		logger.info(self.instance)
		self.instance.status = self.cleaned_data["status"]
		self.instance._additional_data = {
			"Feedback": feedback
		}
		self.instance.save()
		return self.instance

