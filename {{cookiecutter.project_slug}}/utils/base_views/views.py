from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    RedirectView
)
from django.urls import reverse_lazy
from django.contrib import messages

import logging
logger = logging.getLogger(__name__)

# Create your views here.
class BaseListView(ListView):
	pass

class BaseCreateView(CreateView):
	pass

class BaseDetailView(DetailView):
	pass

class BaseUpdateView(UpdateView):
	def form_valid(self, form):
		obj = form.save(commit=False)
		if hasattr(self.model, 'updated_by'):
			obj.updated_by = self.request.user
		obj.save()
		return redirect(self.get_success_url())

class BaseDeleteView(DeleteView):
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