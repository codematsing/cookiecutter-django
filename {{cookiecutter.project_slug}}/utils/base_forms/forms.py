from django import forms
from django.forms.widgets import HiddenInput


class BaseModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		disabled_fields = set(getattr(self.Meta, 'disabled_fields', []))
		hidden_fields = set(getattr(self.Meta, 'hidden_fields', []))
		fields = set(getattr(self.Meta, 'fields', []))
		if self.Meta.fields != '__all__':
			self.Meta.fields = (self.Meta.fields 
				  + list(disabled_fields.difference(fields))
				  + list(hidden_fields.difference(fields))
				  )
		super().__init__(*args, **kwargs)
		try:
			for elem in hidden_fields:
				self.fields[elem].widget = HiddenInput()
				self.fields[elem].disabled = True
			for elem in disabled_fields:
				self.fields[elem].disabled = True
		except Exception as e:
			pass