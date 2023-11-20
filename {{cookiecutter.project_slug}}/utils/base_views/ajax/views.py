from django.views.generic import View
from ajax_datatable.views import AjaxDatatableView
from django.http import JsonResponse
from django.template.loader import render_to_string
from guardian.shortcuts import get_objects_for_user
from urllib.parse import parse_qs
import json

import logging
logger = logging.getLogger(__name__)

class BaseListAjaxView(AjaxDatatableView):
	# show_column_filters=False
	# refer to https://github.com/morlandi/django-ajax-datatable#16column_defs-customizations
	column_defs = [
		{'name':'pk', 'visible':False},
		{'name':'name'},
		{'name':'action', 'searchable':False},
	]

	def list_autofilter_choices(self, request, column_spec, field, initial_search_value):
		qs = self.get_initial_queryset(request)
		if column_spec['name'] in self.model._meta.fields and hasattr(self.model._meta.get_field(column_spec['name']), 'related_model'):
			return [(str(item), str(item)) for item in qs.values_list(column_spec['name'], flat=True).distinct()]
		elif foreign_field := column_spec.get('foreign_field', False):
			return [(str(item), str(item)) for item in qs.values_list(column_spec['foreign_field'], flat=True).distinct()]
		return super().list_autofilter_choices(request, column_spec, field, initial_search_value)

	def sort_queryset(self, params, qs):
		if ordering := getattr(self.model._meta, 'ordering'):
			return qs.order_by(*ordering)
		return super().sort_queryset(params, qs)

	def get_column_defs(self, request):
		column_defs = super().get_column_defs(request)
		hidden = request.REQUEST.get('hidden')
		if hidden not in ['null', None]:
			for col_item in column_defs:
				if col_item['name'] in json.loads(hidden):
					col_item['visible'] = False
		return column_defs

	def filter_queryset_all_columns(self, search_value, qs):
		searchable_columns = [c['name'] for c in self.column_specs if c['searchable'] and c['name']!='action']
		return self._filter_queryset(searchable_columns, search_value, qs, True)

	def filter_qs_from_params(self, request, qs):
		params = parse_qs(request.REQUEST.get('forward'))
		if params:
			pass
		return qs

	def filter_qs_from_data(self, request, qs):
		query = request.REQUEST.get('query')
		if query:
			if query_dict := json.loads(query):
				qs = qs.filter(**query_dict)
		return qs

	def get_initial_queryset(self, request):
		qs = self.model.objects.filter()
		qs = self.filter_qs_from_params(request, qs)
		qs = self.filter_qs_from_data(request, qs)
		return qs

	def get_update_permission(self):
		update_permission = f"{self.model._meta.app_label}.change_{self.model._meta.model_name}"
		return update_permission

	def customize_row(self, row, obj):
		row['action'] = render_to_string('tables/action_column.html', {'record':obj, 'has_update_permission':self.get_update_permission()}) 
		return

class SelectableListAjaxView(BaseListAjaxView):

	def get_column_defs(self, request):
		column_defs = super().get_column_defs(request)
		if not any(filter(lambda col: col['name']=='select', column_defs)):
			column_defs.insert(1, {'name':'select', 'title': 'Select', 'width':'1rem', 'choices':((True, 'Selected'), (False, 'Deselected'))})
		return column_defs

	def customize_row(self, row, obj):
		super().customize_row(row, obj)
		row['select'] = f'<input type="checkbox" class="datatable-checkbox" name="select" width="5rem" value={obj.pk}>'
		return
	pass

class BaseCreateAjaxView(View):
	def get(self, request):
		# get form details
		data = {}
		pk = self.request.GET.get('id', None)
		form = {}
		if form and self.model:
			obj = self.model.object.get(pk=pk).update(**form)
			data['object'] = obj
		return JsonResponse(data)

class BaseDetailAjaxView(View):
	def get(self, request):
		pk = self.request.GET.get('id', None)
		if self.model:
			obj = self.model.object.get(pk=pk)
		data = {
			'object':obj
		}
		return JsonResponse(data)

class BaseUpdateAjaxView(View):
	def get(self, request):
		# get form details
		data = {}
		pk = self.request.GET.get('id', None)
		form = {}
		if form and self.model:
			obj = self.model.object.get(pk=pk).update(**form)
			data['object'] = obj
		return JsonResponse(data)

class BaseDeleteAjaxView(View):
	def get(self, request):
		data = {}
		pk = request.GET.get('id', None)
		if self.model:
			self.model.objects.get(pk=pk).delete()
			data['deleted'] = True
		return JsonResponse(data)

class BaseActionAjaxView(View):
	def get(self, request):
		data = {}
		pk = self.request.GET.get('id', None)
		if self.model:
			obj = self.model.object.get(pk=pk)
			data['object']=obj
		return JsonResponse(data)

class BaseAddObjectAjaxView(View):
	related_name = None
	def get(self, request):
		data = {}
		pk = self.request.GET.get('id', None)
		fk_pk = self.request.GET.get('fk', None)
		if self.model:
			obj = self.model.object.get(pk=pk)
			if self.related_name:
				_set = getattr(self.related_name, obj)
				_set.add(fk_pk)
				data['added'] = True
		return JsonResponse(data)

class BaseRemoveObjectAjaxView(View):
	related_name = None
	def get(self, request):
		data = {}
		pk = self.request.GET.get('id', None)
		fk_pk = self.request.GET.get('fk', None)
		if self.model:
			obj = self.model.object.get(pk=pk)
			if self.related_name:
				_set = getattr(self.related_name, obj)
				_set.remove(fk_pk)
				data['deleted'] = True
		return JsonResponse(data)

class BaseActionObjectAjaxView(View):
	def get(self, request):
		pk = self.request.GET.get('id', None)
		fk_pk = self.request.GET.get('fk', None)
		if self.model:
			obj = self.model.object.get(pk=pk)
		data = {
			'object':obj
		}
		return JsonResponse(data)
