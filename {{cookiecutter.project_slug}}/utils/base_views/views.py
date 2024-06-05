from django import forms
from django.views.generic import (
	ListView,
	CreateView,
	UpdateView,
	RedirectView,
	DeleteView,
)
from django.db.models.deletion import ProtectedError
from django.views.generic.detail import SingleObjectMixin
from utils.base_forms.forms import PdfFileWidget, ImageFileWidget
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from formset.views import (
	FormViewMixin,
	FileUploadMixin,
	FormCollectionView,
	IncompleteSelectResponseMixin,
)
from formset.widgets import UploadedFileInput
from django.forms.fields import FileField, ImageField
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy, resolve
from django.contrib import messages
from formset.renderers.bootstrap import FormRenderer
from utils.detail_wrapper.views import DetailView, DetailWrapperMixin
import json

import logging
logger = logging.getLogger(__name__)

class BaseFormMixin(IncompleteSelectResponseMixin, SuccessMessageMixin, FormViewMixin, FileUploadMixin):
	success_message = "%(object)s has been saved"

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
		if hasattr(self.model, 'updated_by') and (self.form_class or ('updated_by' in self.fields or self.fields=='__all__')):
			initial['updated_by'] = self.request.user
		return initial

	def get_form_kwargs(self):
		extra_data = self.get_extra_data()
		if extra_data and 'is_draft' in extra_data:
			self.form_kwargs = self.form_kwargs or {}
			self.form_kwargs.update({'is_draft': extra_data['is_draft']})
		return super().get_form_kwargs()

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
			if type(field) in [FileField]:
				field.widget = PdfFileWidget()
				field.help_text = f'{getattr(field, "help_text", "")}\nAccepts only PDF. Maximum of 10MB'
			if type(field) in [ImageField]:
				field.widget = ImageFileWidget()
				field.help_text = f'{getattr(field, "help_text", "")}\nAccepts only .png, .jpeg. Maximum of 1MB'
		if getattr(self, 'form_class', None)==None:
			# forces rendering of form to similar to crispy form tags
			setattr(form, 'renderer', FormRenderer())
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
		extra_data = self.get_extra_data()
		extras = {key: val for (key, val) in extra_data.items() if "is_draft" == key} if extra_data else {}
		if extras == {}:
			self.object = form.save()
		else:
			self.object = form.save(extras)
		success_message = self.get_success_message({'object': str(self.object)})
		messages.success(self.request, success_message)
		return JsonResponse({'success_url': self.get_success_url()})

	def form_invalid(self, form):
		logger.error(form._errors.get_json_data())
		return super().form_invalid(form)
	
	def get_form_header(self):
		default = f"{self.model._meta.verbose_name} Form"
		return getattr(self, 'form_header', default)

	def get_button_names(self):
		return {
			"save": getattr(self, 'save_button_text', "Save"),
			"save_as_draft": getattr(self, 'save_as_draft_button_text', "Save as Draft"),
			"cancel": getattr(self, 'cancel_button_text', "Cancel"),
			"modal_negative": getattr(self, 'modal_negative_button_text', "Continue Editing"),
			"modal_positive": getattr(self, 'modal_positive_button_text', "Validate and Submit"),
		}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["form_header"] = self.get_form_header()
		context["enable_save_as_draft"] = getattr(self, 'save_as_draft_enabled', False)
		context["enable_save_modal"] = getattr(self, 'save_modal_enabled', False)
		context["button_names"] = self.get_button_names()
		context["modal_confimation_message"] = getattr(self, 'modal_confimation_message', None)
		return context

class BaseMixin:
	def get_header_buttons(self):
		"""List of urls that is contained in header button

		Returns:
			list[dict]: [{'icon': 'mdi-... 'label': '...', 'href': '#'}]
		"""
		if hasattr(self, 'header_buttons'):
			return self.header_buttons
		return []

	def get_page_title(self):
		if hasattr(self, 'page_title'):
			return self.page_title
		return self.model._meta.verbose_name_plural

	def get_breadcrumbs(self):
		def get_next_breadcrumb(route_list, last):
			route_path = f"/{'/'.join(route_list)}/"
			try:
				match = resolve(route_path)
				label = getattr(match.func.view_class, "breadcrumb_name", None)
				if label is None:
					if match.url_name=="detail":
						label=str(match.func.view_class.model.objects.get(pk=route_list[-1]))
					elif match.url_name=="create":
						label="Create"
					elif match.url_name=="update":
						label="Edit"
					else:
						label = match.func.view_class.model._meta.verbose_name_plural.title()
				if last:
					route_path = "#"
				return {label:route_path}
			except Exception as e:
				print(f"\n no resolve for {route_path}\n{e}")
				return {}

		if not getattr(self, 'breadcrumbs', None):
			route = self.request.get_full_path().strip("/").split("/")
			breadcrumbs = {}
			for index in range(len(route)):
				breadcrumbs.update(get_next_breadcrumb(route[:index+1], len(route)==len(route[:index+1])))
			self.breadcrumbs = breadcrumbs
		return self.breadcrumbs


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["page_title"] = self.get_page_title()
		context["breadcrumbs"] = self.get_breadcrumbs()
		context["header_buttons"] = self.get_header_buttons()
		return context

class BaseFormCollectionView(SuccessMessageMixin, BaseMixin, FormCollectionView):
	template_name = "pages/form.html"
	# follow form collection get_field format: nested '.'
	disabled_fields = []
	hidden_fields = []
	success_message = "%(object)s has been saved"

	def get_form_header(self):
		default = f"{self.model._meta.verbose_name} Form"
		return getattr(self, 'form_header', default)

	def get_save_as_draft_enabled(self):
		return getattr(self, 'save_as_draft_enabled', False)

	def get_save_modal_enabled(self):
		return getattr(self, 'save_modal_enabled', False)

	def get_button_names(self):
		return {
			"save": getattr(self, 'save_button_text', "Save"),
			"save_as_draft": getattr(self, 'save_as_draft_button_text', "Save as Draft"),
			"cancel": getattr(self, 'cancel_button_text', "Cancel"),
			"modal_negative": getattr(self, 'modal_negative_button_text', "Continue Editing"),
			"modal_positive": getattr(self, 'modal_positive_button_text', "Validate and Submit"),
		}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["form_header"] = self.get_form_header()
		context["enable_save_as_draft"] = getattr(self, 'save_as_draft_enabled', False)
		context["enable_save_modal"] = getattr(self, 'save_modal_enabled', False)
		context["button_names"] = self.get_button_names()
		context["modal_confimation_message"] = getattr(self, 'modal_confimation_message', None)
		logger.info(context)
		return context

	def get_collection_kwargs(self):
		extra_data = self.get_extra_data()
		self.collection_kwargs = self.collection_kwargs or {}
		if extra_data and 'is_draft' in extra_data:
			self.collection_kwargs.update({'is_draft': extra_data['is_draft']})
		if hasattr(self, "object"):
			self.collection_kwargs.update({'object': self.object})
		return super().get_collection_kwargs()

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
			for field in self.disabled_fields:
				self.disable_field(form_collection.get_field(field))
		if hasattr(self, 'hidden_fields'):
			for field in self.hidden_fields:
				self.hide_field(form_collection.get_field(field))
		return form_collection

	def get_success_url(self):
		# return None #debug
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
		logger.warning(form_collection._errors)
		return super().form_collection_invalid(form_collection)

	def form_collection_valid(self, form_collection, state=None):
		logger.info("valid form collection")
		extra_data = self.get_extra_data()
		extras = {key: val for (key, val) in extra_data.items() if "is_draft" == key} if extra_data else {}
		if not state:
			self.object = form_collection.save(extras)
		elif state == "create":
			self.object = form_collection.create(extras)
		elif state =="update":
			self.object = form_collection.update(extras)
		success_message = self.get_success_message({'object': str(self.object)})
		messages.success(self.request, success_message)
		return JsonResponse({'success_url': self.get_success_url()})


class BaseCreateFormCollectionView(BaseFormCollectionView):
	success_message = "%(object)s has been created"

	def form_collection_valid(self, form_collection):
		return super().form_collection_valid(form_collection, "create")

class BaseUpdateFormCollectionView(SingleObjectMixin, BaseFormCollectionView):
	success_message = "%(object)s has been updated"

	def form_collection_valid(self, form_collection):
		return super().form_collection_valid(form_collection, "update")

	def get_form_header(self):
		default = f"{self.get_object()} Update Form"
		return getattr(self, 'form_header', default)

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
		ajax_url = "#"
		try:
			ajax_url = self.model.get_ajax_list_url()
		except Exception as e:
			logger.error(e)
		return ajax_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["ajax_list_url"] = self.get_ajax_list_url()
		context["hidden"] = self.get_hidden_ajax_columns()
		context["query"] = self.get_json_query()
		return context


class BaseListView(BaseWAjaxDatatableMixin, BaseMixin, ListView):
	template_name='pages/list.html'

	def get_header_buttons(self):
		add_url = "#"
		try:
			add_url = self.model.get_create_url()
		except Exception as e:
			logger.error(e)
		return [
			{'label':'Add', 'icon':'mdi-plus', 'href':add_url}
		]

class BaseCreateView(BaseMixin, BaseFormMixin, CreateView):
	template_name='pages/create.html'
	fields = '__all__'
	disabled_fields=['updated_by']
	success_message = "%(object)s has been created"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if 'page_title' not in context.keys():
			context["page_title"] = f"{self.model._meta.verbose_name} Create Form"
		return context

class BaseDetailView(BaseMixin, DetailView):
	template_name='pages/detail.html'
	fields = '__all__'
	extra_context = {'show_action_buttons':True}

	def get_header_buttons(self):
		update_url = "#"
		try:
			update_url = self.get_object().get_update_url()
		except Exception as e:
			logger.error(e)
		return [
			{'label':'Edit', 'icon':'mdi-pencil', 'href':update_url}
		]

	def get_page_title(self):
		return str(self.get_object())

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

class BaseUpdateView(BaseMixin, BaseFormMixin, UpdateView):
	template_name='pages/update.html'
	fields = '__all__'
	disabled_fields=['updated_by']
	success_message = "%(object)s has been updated"

	def get_form(self, form_class=None):
		return super(BaseFormMixin, self).get_form(form_class)

	def get_page_title(self):
		return str(self.get_object())

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

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
		return reverse_lazy(f"{':'.join(self.request.resolver_match.namespaces)}:list")

	def delete(self, request, *args, **kwargs):
		try:
			return super().delete(request, *args, **kwargs)
		except ProtectedError:
			messages.error(self.request, f"Cannot delete {self.object}. There exists references to this object.")
			url = reverse(f"{':'.join(self.request.resolver_match.namespaces)}:delete", kwargs={"pk": self.kwargs['pk']})
			return HttpResponseRedirect(url)

	def post(self, request, *args, **kwargs):
		return self.delete(request, *args, **kwargs)

class BaseActionView(RedirectView):
	pass

class BaseAddObjectView(RedirectView):
	pass

class BaseRemoveObjectView(RedirectView):
	pass

class BaseActionObjectView(RedirectView):
	pass
