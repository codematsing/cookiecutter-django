from django import forms
from django.forms.widgets import HiddenInput
from formset.renderers.bootstrap import FormRenderer
from formset.collection import FormCollection
from django.contrib.auth import get_user_model
from utils.validators import EmailValidator
from formset.widgets import Selectize, SelectizeMultiple, DualSelector
import logging
logger = logging.getLogger(__name__)
class CustomSelectize(Selectize):
    max_prefetch_choices = 600
	# customize due to cap of original

class CustomSelectizeMultiple(SelectizeMultiple):
    max_prefetch_choices = 600
	# customize due to cap of original

class CustomDualSelector(DualSelector):
    max_prefetch_choices = 600
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

class BaseModelForm(forms.ModelForm):
	default_renderer = FormRenderer
	is_draft = None

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
		self.set_disabled_fields(kwargs)
		self.set_hidden_fields(kwargs)
		self.set_meta_fields()
		if 'is_draft' in kwargs:
			self.is_draft = kwargs.pop('is_draft', None)
		super().__init__(*args, **kwargs)
		self.disable_fields(self.disabled_fields)
		self.hide_fields(self.hidden_fields)

class BaseFormCollection(FormCollection):
	default_renderer = FormRenderer
	is_draft = None

	def __init__(self, **kwargs):
		if 'is_draft' in kwargs:
			self.is_draft = kwargs.pop('is_draft', None)
		super().__init__(**kwargs)

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

	def save(self, extras={}, *args, **kwargs):
		raise NotImplementedError("Need to provide saving mechanism for Form")

	def create(self, extras={}):
		return self.save(extras)

	def update(self, extras={}):
		return self.save(extras)

		
	#TODO: form collection hidden and disabled fields