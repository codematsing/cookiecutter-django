from django import forms
from django.views.generic import (
	ListView,
	CreateView,
	UpdateView,
	RedirectView,
	DeleteView,
)
from django.views.generic.detail import SingleObjectMixin
from django.http import JsonResponse
from formset.views import FormViewMixin, FileUploadMixin, FormCollectionView
from formset.widgets import UploadedFileInput
from django.forms.fields import FileField, ImageField
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from utils.detail_wrapper.views import DetailView, DetailWrapperMixin
import json

import logging
logger = logging.getLogger(__name__)

class BaseFormMixin(FormViewMixin, FileUploadMixin):
	def __init__(self, *args, **kwargs):
		if self.form_class == None:
			disabled_fields = set(getattr(self, 'disabled_fields', [])).intersection(set(field.name for field in self.model._meta.fields))
			hidden_fields = set(getattr(self, 'hidden_fields', [])).intersection(set(field.name for field in self.model._meta.fields))
			fields = set(getattr(self, 'fields', []))
			if self.fields != '__all__':
				self.fields = (self.fields 
					+ list(disabled_fields.difference(fields))
					+ list(hidden_fields.difference(fields))
					)
		else: #form_class is set
			self.fields = None
		return super().__init__(*args, **kwargs)

	def get_initial(self):
		initial = super().get_initial()
		if not self.form_class and hasattr(self.model, 'updated_by') and ('updated_by' in self.fields or self.fields=='__all__'):
			initial['updated_by'] = self.request.user
		return initial

	def get_hidden_fields(self):
		return getattr(self, 'hidden_fields', [])

	def get_disabled_fields(self):
		return getattr(self, 'disabled_fields', [])

	def disable_field(self, form, field_name):
		if field_name in form.fields:
			form.fields[field_name].disabled = True
		return form

	def hide_field(self, form, field_name):
		if field_name in form.fields:
			self.disable_field(form, field_name)
			form.fields[field_name].widget = forms.HiddenInput()
		return form

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		for field in self.get_hidden_fields():
			self.hide_field(form, field)
		for field in self.get_disabled_fields():
			self.disable_field(form, field)
		for field in form.fields.values():
			if type(field) in [FileField, ImageField]:
				field.widget = UploadedFileInput()
		return form

	def get_success_url(self):
		http_meta = self.request.META.get('HTTP_REFERER', None)
		if success_url := super().get_success_url():
			logger.info(f"DEFAULTS to {self.__class__.__name__}'s success_url: {self.success_url}")
			self.success_url = success_url
		elif _object := getattr(self, 'object', None):
			logger.info(f"1st FALLBACK to object instance: {_object}")
			self.success_url = _object.get_absolute_url()
		elif self.request.get_full_path() != http_meta:
			logger.info(f"2nd FALLBACK to HTTP REFERER: {http_meta}")
			self.success_url = http_meta
		else:
			try:
				list_url = reverse_lazy(f"{':'.join(self.request.resolver_match.namespaces)}:list", kwargs=self.kwargs)
				logger.info(f"3rd FALLBACK to {self.__class__.__name__}'s list view: {list_url}")
			except Exception as e:
				self.success_url = list_url
				logger.warning(f"""
				FALLBACK SUCCESS URL to home
				HTTP_REFERER: {http_meta}
				No success url for fallback
				Fallback url does not exist. See Traceback
				""")
				logger.exception(e)
				self.success_url = reverse_lazy('home')
				messages.warning("Rerouted to home. No url provided")
		logger.info(f"SUCCESS URL: {self.success_url}")
		return self.success_url

	def form_valid(self, form):
		self.object = form.save()
		messages.success(self.request, f"{self.object} has been saved")
		return JsonResponse({'success_url': self.get_success_url()})

class BaseMixin:
	def get_header_buttons(self):
		"""List of urls that is contained in header button

		Returns:
			list(dict): ['icon': 'mdi-... 'label': '...', 'href': '#']
		"""
		if hasattr(self, 'header_buttons'):
			return self.header_buttons
		return []

	def get_page_title(self):
		if hasattr(self, 'page_title'):
			return self.page_title
		return self.model._meta.verbose_name_plural

	def get_breadcrumbs(self):
		"""Dict for breadcrumbs

		Returns:
			dict: ['parent_label':'parent_href', 'child_label':'child_href']
		"""
		if hasattr(self, 'breadcrumbs'):
			return self.breadcrumbs
		return {}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["page_title"] = self.get_page_title()
		context["breadcrumbs"] = self.get_breadcrumbs()
		context["header_buttons"] = self.get_header_buttons()
		return context

class BaseFormCollectionView(BaseMixin, FormCollectionView):
	template_name = "pages/form.html"
	def disable_field(self, field):
		field.widget.attrs.update({'disabled':True})
		return field

	def hide_field(self, field):
		# self.disable_field(field)
		field.widget = forms.HiddenInput()
		return field

	def get_form_collection(self):
		form_collection = super().get_form_collection()
		if hasattr(self, 'disabled_fields'):
			for form_name, d_fields in self.disabled_fields.items():
				for field_name in d_fields:
					field = form_collection.get_field(f'{form_name}.{field_name}')
					self.disable_field(field)
		if hasattr(self, 'hidden_fields'):
			for form_name, h_fields in self.hidden_fields.items():
				for field_name in h_fields:
					field = form_collection.get_field(f'{form_name}.{field_name}')
					logger.info(field)
					self.hide_field(field)
		return form_collection

	def get_success_url(self):
		http_meta = self.request.META.get('HTTP_REFERER', None)
		if success_url := super().get_success_url():
			logger.info(f"DEFAULTS to {self.__class__.__name__}'s success_url: {self.success_url}")
			self.success_url = success_url
		elif _object := getattr(self, 'object', None):
			logger.info(f"1st FALLBACK to object instance: {_object}")
			self.success_url = _object.get_absolute_url()
		elif self.request.get_full_path() != http_meta:
			logger.info(f"2nd FALLBACK to HTTP REFERER: {http_meta}")
			self.success_url = http_meta
		else:
			try:
				list_url = reverse_lazy(f"{':'.join(self.request.resolver_match.namespaces)}:list", kwargs=self.kwargs)
				logger.info(f"3rd FALLBACK to {self.__class__.__name__}'s list view: {list_url}")
			except Exception as e:
				self.success_url = list_url
				logger.warning(f"""
				FALLBACK SUCCESS URL to home
				HTTP_REFERER: {http_meta}
				No success url for fallback
				Fallback url does not exist. See Traceback
				""")
				logger.exception(e)
				self.success_url = reverse_lazy('home')
				messages.warning("Rerouted to home. No url provided")
		logger.info(f"SUCCESS URL: {self.success_url}")
		return self.success_url

	def form_collection_invalid(self, form_collection):
		logger.warning(vars(form_collection))
		return super().form_collection_invalid(form_collection)

	def form_collection_valid(self, form_collection):
		self.object = form_collection.save()
		messages.success(self.request, f"{self.object} has been saved")
		return JsonResponse({'success_url': self.get_success_url()})

class BaseCreateFormCollectionView(BaseFormCollectionView):
	def form_collection_valid(self, form_collection):
		self.object = form_collection.create()
		return super().form_collection_valid(form_collection)

	def form_collection_valid(self, form_collection):
		self.object = form_collection.create()
		messages.success(self.request, f"{self.object} has been created")
		return JsonResponse({'success_url': self.get_success_url()})

class BaseUpdateFormCollectionView(BaseFormCollectionView, SingleObjectMixin):
	def form_collection_valid(self, form_collection):
		self.object = form_collection.update()
		messages.success(self.request, f"{self.object} has been updated")
		return JsonResponse({'success_url': self.get_success_url()})

	def get_context_data(self, **kwargs):
		self.object = self.get_object()
		return super().get_context_data(**kwargs)

class BaseWAjaxDatatableMixin:
	hidden_columns = []
	json_query = {}
	def get_json_query(self, _dict=dict()):
		"""Passes a dictionary that will be accepted by the ajaxurl
		Will be processed by AjaxListView.filter_qs_from_data
  		"""
		_dict = _dict or self.json_query
		if _dict:
			return json.dumps(_dict)
		else:
			return json.dumps(None)

	def get_hidden_ajax_columns(self, _list=list()):
		"""Passes a dictionary that will be accepted by the ajaxurl
		Will be processed by AjaxListView.filter_qs_from_data
  		"""
		_list = _list or self.hidden_columns
		if _list:
			return json.dumps(_list)
		else:
			return json.dumps(None)
	
	def get_ajax_list_url(self):
		"""Ajax list url that will be processed in template view
  		"""
		ajax_url = f"{self.request.resolver_match.namespace}:ajax:list"
		return reverse_lazy(ajax_url, kwargs=self.kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["ajax_list_url"] = self.get_ajax_list_url()
		context["hidden"] = self.get_hidden_ajax_columns()
		context["query"] = self.get_json_query()
		return context


class BaseListView(BaseWAjaxDatatableMixin, BaseMixin, ListView):
	template_name='pages/list.html'

	def get_breadcrumbs(self):
		self.breadcrumbs = {self.get_page_title(): self.request.path}
		return super().get_breadcrumbs()

	def get_header_buttons(self):
		add_url = reverse_lazy(
			":".join(self.request.resolver_match.namespaces)+":create", kwargs=self.kwargs
		)
		return [
			{'label':'Add', 'icon':'mdi-plus', 'href':add_url}
		]

class BaseCreateView(BaseMixin, BaseFormMixin, CreateView):
	template_name='pages/create.html'
	fields = '__all__'
	disabled_fields=['updated_by']

	def get_breadcrumbs(self):
		list_url = reverse_lazy(
			":".join(self.request.resolver_match.namespaces)+":list", kwargs=self.kwargs
		)
		self.breadcrumbs = {
			self.get_page_title(): list_url,
			'Create': self.request.path,
		}
		return super().get_breadcrumbs()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if 'page_title' not in context.keys():
			context["page_title"] = f"{self.model._meta.verbose_name} Create Form"
		return context

	def form_valid(self, form):
		self.object = form.save()
		messages.success(self.request, f"{self.object} has been created")
		return JsonResponse({'success_url': self.get_success_url()})


class BaseDetailView(BaseMixin, DetailView):
	template_name='pages/detail.html'
	fields = '__all__'
	extra_context = {'show_action_buttons':True}

	def get_header_buttons(self):
		update_url = reverse_lazy(
			":".join(self.request.resolver_match.namespaces)+":update", kwargs=self.kwargs
		)
		return [
			{'label':'Edit', 'icon':'mdi-pencil', 'href':update_url}
		]

	def get_breadcrumbs(self):
		_object = self.get_object()
		model_name = self.model._meta.verbose_name_plural
		namespace = ":".join(self.request.resolver_match.namespaces)
		self.breadcrumbs = {
			model_name:reverse_lazy(f'{namespace}:list'),
			f'{_object}':reverse_lazy(f'{namespace}:detail', kwargs=self.kwargs),
		}
		return super().get_breadcrumbs()

	def get_page_title(self):
		return str(self.get_object())

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

class BaseUpdateView(BaseMixin, BaseFormMixin, UpdateView):
	template_name='pages/update.html'
	fields = '__all__'
	disabled_fields=['updated_by']

	def get_breadcrumbs(self):
		_object = self.get_object()
		model_name = self.model._meta.verbose_name_plural
		namespace = ":".join(self.request.resolver_match.namespaces)
		self.get_breadcrumbs = {
			model_name:f'{namespace}:list',
			f'{_object}':reverse_lazy('posts:detail', kwargs=self.kwargs),
			'Edit':reverse_lazy('posts:update', kwargs=self.kwargs),
		}
		return super().get_breadcrumbs()

	def get_page_title(self):
		return str(self.get_object())

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def form_valid(self, form):
		self.object = form.save()
		messages.success(self.request, f"{self.object} has been updated")
		return JsonResponse({'success_url': self.get_success_url()})

class BaseDeleteView(BaseMixin, DetailWrapperMixin, DeleteView):
	template_name = 'pages/delete.html'
	accept_global_perms = True
	extra_context = {'show_action_buttons':False}

	def get_page_title(self):
		return str(self.get_object())

	def get_context_data(self, *arg, **kwargs):
		context = super().get_context_data(*arg, **kwargs)
		context["fields"] = self.get_rendered_fields_items()
		return context

	def get_success_url(self):
		return reverse_lazy(f"{':'.join(self.request.resolver_match.namespaces)}:list", kwargs=self.kwargs)
		
class BaseActionView(RedirectView):
	pass

class BaseAddObjectView(RedirectView):
	pass

class BaseRemoveObjectView(RedirectView):
	pass

class BaseActionObjectView(RedirectView):
	pass