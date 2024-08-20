from django import forms
from django.shortcuts import redirect
from django.views.generic import (
	ListView,
	CreateView,
	UpdateView,
	RedirectView,
)
from django.utils.text import slugify
from django.views.generic.detail import SingleObjectMixin
from django.http import JsonResponse
from formset.views import FormViewMixin, FileUploadMixin, FormCollectionView
from utils.base_forms.forms import PdfFileWidget, ImageFileWidget
from django.forms.fields import FileField, ImageField
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy, resolve
from django.contrib import messages
from formset.renderers.bootstrap import FormRenderer
from utils.detail_wrapper.views import DetailView, DetailWrapperMixin
from utils.base_forms.forms import DeleteForm
import json

import logging

logger = logging.getLogger(__name__)

class RestrictFileUploadType:
	"""To be placed in areas with FileUploadMixin
	"""
	restricted_content_types = ["application/pdf", "image/png", "image/jpeg"]

	def _receive_uploaded_file(self, file_obj, image_height=None):
		response = super()._receive_uploaded_file(file_obj, image_height)
		_data = json.loads(response.content)
		if not self.restricted_content_types or _data['content_type'] in self.restricted_content_types:
			return response


class BaseFormMixin(RestrictFileUploadType, SuccessMessageMixin, FormViewMixin, FileUploadMixin):
	def __init__(self, *args, **kwargs):
		if self.form_class == None:
			disabled_fields = set(getattr(self, "disabled_fields", [])).intersection(
				set(field.name for field in self.model._meta.fields)
			)
			hidden_fields = set(getattr(self, "hidden_fields", [])).intersection(
				set(field.name for field in self.model._meta.fields)
			)
			fields = set(getattr(self, "fields", []))
			if self.fields != "__all__":
				self.fields = (
					self.fields
					+ list(disabled_fields.difference(fields))
					+ list(hidden_fields.difference(fields))
				)
		else:  # form_class is set
			self.fields = None
		return super().__init__(*args, **kwargs)

	def get_form_header(self):
		default = ""
		try:
			default = f"{self.model._meta.verbose_name} Form"
		except Exception as e:
			pass
		return getattr(self, "form_header", default)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["form_header"] = self.get_form_header()
		return context

	def get_extra_data(self):
		extra_data = super().get_extra_data() or {}
		extra_data.update({
			'request': self.request
		})
		return extra_data

	def get_form_kwargs(self):
		form_kwargs = super().get_form_kwargs()
		if self.form_class:
			form_kwargs.update({'extra_data':self.get_extra_data()})
		return form_kwargs

	def get_hidden_fields(self):
		return getattr(self, "hidden_fields", [])

	def get_disabled_fields(self):
		return getattr(self, "disabled_fields", [])

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
		if not vars(form.renderer):
			# forces rendering of form to similar to crispy form tags
			setattr(form, "renderer", FormRenderer())
		return form

	def get_success_url(self):
		http_meta = self.request.META.get("HTTP_REFERER", None)
		if success_url := super().get_success_url():
			logger.info(
				f"DEFAULTS to {self.__class__.__name__}'s success_url: {self.success_url}"
			)
			self.success_url = success_url
		elif _object := getattr(self, "object", None):
			logger.info(f"1st FALLBACK to object instance: {_object}")
			self.success_url = _object.get_absolute_url()
		elif self.request.get_full_path() != http_meta:
			logger.info(f"2nd FALLBACK to HTTP REFERER: {http_meta}")
			self.success_url = http_meta
		else:
			try:
				list_url = reverse_lazy(
					f"{':'.join(self.request.resolver_match.namespaces)}:list",
					kwargs=self.kwargs,
				)
				logger.info(
					f"3rd FALLBACK to {self.__class__.__name__}'s list view: {list_url}"
				)
			except Exception as e:
				self.success_url = list_url
				logger.warning(
					f"""
				FALLBACK SUCCESS URL to home
				HTTP_REFERER: {http_meta}
				No success url for fallback
				Fallback url does not exist. See Traceback
				"""
				)
				logger.exception(e)
				self.success_url = reverse_lazy("home")
				messages.warning("Rerouted to home. No url provided")
		logger.info(f"SUCCESS URL: {self.success_url}")
		return self.success_url

	def form_valid(self, form):
		self.object = form.save()
		messages.success(self.request, f"{self.object} has been saved")
		return JsonResponse({"success_url": self.get_success_url()})

	def form_invalid(self, form):
		logger.info(vars(form))
		logger.info(form.errors)
		return super().form_invalid(form)


class BaseMixin:
	def get_header_buttons(self):
		"""List of urls that is contained in header button

		Returns:
				list[dict]: [{'icon': 'mdi-... 'label': '...', 'href': '#'}]
		"""
		if hasattr(self, "header_buttons"):
			return self.header_buttons
		return []

	def get_page_title(self):
		if hasattr(self, "page_title"):
			return self.page_title
		return self.model._meta.verbose_name_plural

	def get_breadcrumbs(self):
		def get_next_breadcrumb(route_list):
			route_path = f"/{'/'.join(route_list)}/"
			try:
				match = resolve(route_path)
				label = match.func.view_class.model._meta.verbose_name_plural.title()
				if match.url_name == "detail":
					last_key = list(match.kwargs.keys())[-1]
					if "_pk" in last_key:
						last_key = "pk"
					label = str(
						match.func.view_class.model.objects.get(**{last_key:match.kwargs[last_key]})
					)
				elif match.url_name == "create":
					label = "Create"
				elif match.url_name == "update":
					label = "Edit"
				return {label: route_path}
			except Exception as e:
				logger.warning(e)
				logger.debug(f"\n no resolve for {route_path}\n")
				if route_path == self.request.path:
					return {self.get_page_title():self.request.get_full_path}
			return {}

		if not getattr(self, "breadcrumbs", None):
			route = self.request.get_full_path().split("?")[0].strip("/").split("/")
			breadcrumbs = {}
			for index in range(len(route)):
				next_breadcrumb = get_next_breadcrumb(route[: index + 1])
				breadcrumbs.update(next_breadcrumb)
			self.breadcrumbs = breadcrumbs
		return self.breadcrumbs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["page_title"] = self.get_page_title()
		context["breadcrumbs"] = self.get_breadcrumbs()
		context["header_buttons"] = self.get_header_buttons()
		return context


class BaseFormCollectionView(RestrictFileUploadType, SuccessMessageMixin, BaseMixin, FormCollectionView):
	template_name = "pages/form.html"
	# follow form collection get_field format: nested '.'
	disabled_fields = []
	hidden_fields = []

	def get(self, request, **kwargs):
		logger.info("TRIGGERED")
		if request.accepts('application/json') and 'field' in request.GET:
			return self._fetch_options(request)
		return super().get(request, **kwargs)

	def _fetch_options(self, request):
		logger.info("FETCH")
		return super()._fetch_options(request)

	def get_form_header(self):
		default = ""
		try:
			default = f"{self.model._meta.verbose_name} Form"
		except Exception as e:
			pass
		return getattr(self, "form_header", default)

	def disable_field(self, field):
		field.widget.attrs.update({"disabled": True})
		return field

	def hide_field(self, field):
		# self.disable_field(field)
		field.widget = forms.HiddenInput()
		return field

	def get_extra_data(self):
		extra_data = super().get_extra_data() or {}
		extra_data.update({
			'request': self.request
		})
		return extra_data 

	def get_collection_kwargs(self):
			kwargs = super().get_collection_kwargs()
			kwargs.update({'extra_data':self.get_extra_data()})
			return kwargs

	def get_form_collection(self):
		form_collection = super().get_form_collection()
		if hasattr(self, "disabled_fields"):
			for field in self.disabled_fields:
				self.disable_field(form_collection.get_field(field))
		if hasattr(self, "hidden_fields"):
			for field in self.hidden_fields:
				self.hide_field(form_collection.get_field(field))
		return form_collection

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["form_header"] = self.get_form_header()
		return context

	def get_success_url(self):
		# return None #debug
		http_meta = self.request.META.get("HTTP_REFERER", None)
		if success_url := super().get_success_url():
			logger.info(
				f"DEFAULTS to {self.__class__.__name__}'s success_url: {self.success_url}"
			)
			self.success_url = success_url
		elif _object := getattr(self, "object", None):
			logger.info(f"1st FALLBACK to object instance: {_object}")
			self.success_url = _object.get_absolute_url()
		elif self.request.get_full_path() != http_meta:
			logger.info(f"2nd FALLBACK to HTTP REFERER: {http_meta}")
			self.success_url = http_meta
		else:
			try:
				list_url = reverse_lazy(
					f"{':'.join(self.request.resolver_match.namespaces)}:list",
					kwargs=self.kwargs,
				)
				logger.info(
					f"3rd FALLBACK to {self.__class__.__name__}'s list view: {list_url}"
				)
			except Exception as e:
				self.success_url = list_url
				logger.warning(
					f"""
				FALLBACK SUCCESS URL to home
				HTTP_REFERER: {http_meta}
				No success url for fallback
				Fallback url does not exist. See Traceback
				"""
				)
				logger.exception(e)
				self.success_url = reverse_lazy("home")
				messages.warning("Rerouted to home. No url provided")
		logger.info(f"SUCCESS URL: {self.success_url}")
		return self.success_url

	def form_collection_invalid(self, form_collection):
		logger.warning(vars(form_collection))
		logger.warning(form_collection._errors)
		return super().form_collection_invalid(form_collection)

	def form_collection_valid(self, form_collection):
		self.object = form_collection.save()
		self.success_message = (
			self.get_success_message(form_collection.cleaned_data)
			or f"{self.object} has been saved"
		)
		messages.success(self.request, self.success_message)
		return JsonResponse({"success_url": self.get_success_url()})


class BaseCreateFormCollectionView(BaseFormCollectionView):
	def form_collection_valid(self, form_collection):
		logger.info("valid form collection")
		self.object = form_collection.create()
		self.success_message = (
			self.get_success_message(form_collection.cleaned_data)
			or f"{self.object} has been created"
		)
		messages.success(self.request, self.success_message)
		return JsonResponse({"success_url": self.get_success_url()})


class BaseUpdateFormCollectionView(BaseFormCollectionView, SingleObjectMixin):

	def form_collection_valid(self, form_collection):
		logger.info("valid form collection")
		self.object = form_collection.update()
		self.success_message = (
			self.get_success_message(form_collection.cleaned_data)
			or f"{self.object} has been updated"
		)
		messages.success(self.request, self.success_message)
		return JsonResponse({"success_url": self.get_success_url()})

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
		"""Ajax list url that will be processed in template view"""
		try:
			return self.model.get_ajax_list_url()
		except Exception as e:
			logger.warning(f"Define get_ajax_list_url for {self}")
			return ""

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["ajax_list_url"] = self.get_ajax_list_url()
		context["hidden"] = self.get_hidden_ajax_columns()
		context["query"] = self.get_json_query()
		return context


class BaseListView(BaseWAjaxDatatableMixin, BaseMixin, ListView):
	template_name = "pages/list.html"

	def get_header_buttons(self):
		add_url = reverse_lazy(
			":".join(self.request.resolver_match.namespaces) + ":create",
			kwargs=self.kwargs,
		)
		return [{"label": "Add", "icon": "mdi-plus", "href": add_url}]


class BaseCreateView(BaseMixin, BaseFormMixin, CreateView):
	template_name = "pages/create.html"
	fields = "__all__"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if "page_title" not in context.keys():
			context["page_title"] = f"{self.model._meta.verbose_name} Create Form"
		return context

	def form_valid(self, form):
		self.object = form.save()
		self.success_message = (
			self.get_success_message(form.cleaned_data)
			or f"{self.object} has been updated"
		)
		messages.success(self.request, self.success_message)
		return JsonResponse({"success_url": self.get_success_url()})


class BaseDetailView(BaseMixin, DetailView):
	template_name = "pages/detail.html"
	fields = "__all__"
	extra_context = {"show_action_buttons": True}

	def get_header_buttons(self):
		update_url = reverse_lazy(
			":".join(self.request.resolver_match.namespaces) + ":update",
			kwargs=self.kwargs,
		)
		delete_url = reverse_lazy(
			":".join(self.request.resolver_match.namespaces) + ":delete",
			kwargs=self.kwargs,
		)
		return [
			{"label": "Edit", "icon": "mdi-pencil", "href": update_url},
			{"label": "Delete", "icon": "mdi-trash-can", "href": delete_url}
		]

	def get_page_title(self):
		return str(self.get_object())

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


class BaseUpdateView(BaseMixin, BaseFormMixin, UpdateView):
	template_name = "pages/update.html"
	fields = "__all__"

	def get_page_title(self):
		return str(self.get_object())

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def form_valid(self, form):
		self.object = form.save()
		self.success_message = (
			self.get_success_message(form.cleaned_data)
			or f"{self.object} has been updated"
		)
		messages.success(self.request, self.success_message)
		return JsonResponse({"success_url": self.get_success_url()})


class BaseDeleteView(BaseUpdateView):
	form_class = DeleteForm 
	template_name = "pages/delete.html"
	accept_global_perms = True
	extra_context = {"show_action_buttons": False}

	def get_initial(self):
		return {"copy_object_str":slugify(str(self.get_object()))}

	def get_form_header(self):
		default = f"{self.model._meta.verbose_name} Delete Form"
		return getattr(self, "form_header", default)

	def get_page_title(self):
		return str(self.get_object())

	def get_form_kwargs(self):
		form_kwargs = super().get_form_kwargs()
		form_kwargs['instance'] = self.get_object()
		return form_kwargs

	def get_context_data(self, *arg, **kwargs):
		context = super().get_context_data(*arg, **kwargs)
		context["form_header"] = self.get_form_header()
		return context

	def get_success_url(self):
		url = reverse("dashboard")
		try:
			pattern = ':'.join(self.request.resolver_match.namespaces)
			logger.info(pattern)
			url = reverse(f"{':'.join(self.request.resolver_match.namespaces)}:list")
		except Exception as e:
			pass
		logger.info(url)
		return url

	def form_valid(self, form):
		self.object.delete()
		success_message = f"{self.object} deleted"
		messages.error(self.request, success_message)
		return JsonResponse({"success_url": self.get_success_url()})

class BaseActionView(RedirectView):
	pass


class BaseAddObjectView(RedirectView):
	pass


class BaseRemoveObjectView(RedirectView):
	pass


class BaseActionObjectView(RedirectView):
	pass
