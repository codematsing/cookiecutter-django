from django.shortcuts import render, redirect
from django import forms
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    RedirectView
)
from django.urls import reverse_lazy
from django.contrib import messages
from utils.detail_wrapper.views import DetailView
from collections import OrderedDict
from dal import autocomplete

import logging
logger = logging.getLogger(__name__)

class BaseForm:
	def __init__(self, *args, **kwargs):
		disabled_fields = set(getattr(self, 'disabled_fields', []))
		hidden_fields = set(getattr(self, 'hidden_fields', []))
		fields = set(getattr(self, 'fields', []))
		if self.fields != '__all__':
			self.fields = (self.fields 
                  + list(disabled_fields.difference(fields))
                  + list(hidden_fields.difference(fields))
                  )
		return super().__init__(*args, **kwargs)

	def get_initial(self):
		initial = super().get_initial()
		if hasattr(self.model, 'updated_by') and ('updated_by' in self.fields or self.fields=='__all__'):
			initial['updated_by'] = self.request.user
		return initial

	def get_hidden_fields(self):
		return getattr(self, 'hidden_fields', [])

	def get_disabled_fields(self):
		return getattr(self, 'disabled_fields', [])

	def disable_field(self, form, field_name):
		form.fields[field_name].disabled = True
		return form

	def hide_field(self, form, field_name):
		self.disable_field(form, field_name)
		form.fields[field_name].widget = forms.HiddenInput()
		return form

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		for field in self.get_hidden_fields():
			self.hide_field(form, field)
		for field in self.get_disabled_fields():
			self.disable_field(form, field)
		return form


# Create your views here.
class BaseListView(ListView):
	template_name='pages/list.html'

class BaseCreateView(BaseForm, CreateView):
	template_name='pages/create.html'
	fields = '__all__'
	disabled_fields=['updated_by']

class BaseDetailView(DetailView):
	template_name='pages/detail.html'
	fields = '__all__'

class BaseUpdateView(BaseForm, UpdateView):
	template_name='pages/update.html'
	fields = '__all__'
	disabled_fields=['updated_by']

class BaseDeleteView(RedirectView):
	# assumption is modal confirmation
	# direct delete without confirmation
	def get(self, request, *args, **kwargs):
		obj = self.get_object()
		url_namespace = self.request.resolver_match.namespace
		self.url = reverse_lazy(f'{url_namespace}:list')
		messages.add_message(self.request, messages.INFO, f'{obj} was deleted.')
		return self.post(request, *args, **kwargs)

	def get_success_url(self, request, *args, **kwargs):
		return self.url
		
class BaseActionView(RedirectView):
	pass

class BaseAddObjectView(RedirectView):
	pass

class BaseRemoveObjectView(RedirectView):
	pass

class BaseActionObjectView(RedirectView):
	pass

class BaseAutocompleteView(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		if not self.request.user.is_authenticated:
			return self.model.objects.none()

		qs = self.model.objects.all()

		if self.q:
			qs = qs.filter(name__istartswith=self.q)

		return qs