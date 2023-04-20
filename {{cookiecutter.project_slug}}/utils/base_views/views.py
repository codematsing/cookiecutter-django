from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    RedirectView
)
from django.urls import reverse_lazy
from django.contrib import messages
from utils.detail_wrapper.views import DetailView

import logging
logger = logging.getLogger(__name__)

class BaseForm:
	def get_initial(self):
		initial = super().get_initial()
		if hasattr(self.model, 'updated_by') and ('updated_by' in self.fields or self.fields=='__all__'):
			initial['updated_by'] = self.request.user
		return initial

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		if 'updated_by' in form.fields.keys():
			form.fields['updated_by'].widget.attrs['readonly'] = True
			form.fields['updated_by'].disabled = True
		return form


# Create your views here.
class BaseListView(ListView):
	template_name='pages/list.html'

class BaseCreateView(BaseForm, CreateView):
	template_name='pages/create.html'
	fields = '__all__'

class BaseDetailView(DetailView):
	template_name='pages/detail.html'
	fields = '__all__'

class BaseUpdateView(BaseForm, UpdateView):
	template_name='pages/update.html'
	fields = '__all__'

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