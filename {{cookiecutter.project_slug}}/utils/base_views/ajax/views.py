from django.views.generic import View
from ajax_datatable.views import AjaxDatatableView
from django.http import JsonResponse
from django.template.loader import render_to_string
from guardian.shortcuts import get_objects_for_user
from urllib.parse import parse_qs

import logging
logger = logging.getLogger(__name__)

class BaseListAjaxView(AjaxDatatableView):
    # show_column_filters=False
    # refer to https://github.com/morlandi/django-ajax-datatable#16column_defs-customizations
    sort_field='-updated_at'
    column_defs = [
        {'name':'pk', 'visible':False},
        {
            'name':'updated_by', 
			'foreign_field': 'updated_by__username',
            'autofilter': True, 
            'initialSearchValue': None
        },
        {'name':'updated_at'},
        {'name':'action'},
    ]
    def filter_qs(self, qs, query_dict):
        return qs

    def get_initial_queryset(self, request):
        query_dict = {}
        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method=='GET' else request.POST
            query_dict = parse_qs(request.REQUEST.get('forward'))
            # no action done in parameters. need to do filter
        try:
            qs =get_objects_for_user(request.user, perms=f"view_{self.model._meta.verbose_name}", klass=self.model)
        except Exception as e:
            logger.exception(e)    
            qs = self.model.objects.all()
        return self.filter_qs(qs, query_dict)

    def customize_row(self, row, obj):
        row['action'] = render_to_string('tables/action_column.html', {'record':obj}) 
        return

class BaseCreateAjaxView(View):
    def get(self, request):
        # get form details
        form = {}
        if form and self.model:
            obj = self.model.object.create(**form)
        data = {
            'object':obj
        }
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
        pk = self.request.GET.get('id', None)
        form = {}
        if form and self.model:
            obj = self.model.object.get(pk=pk).update(**form)
        return JsonResponse(
            {'object':obj}
        )

class BaseDeleteAjaxView(View):
    def get(self, request):
        pk = request.GET.get('id', None)
        if self.model:
            self.model.objects.get(pk=pk).delete()
            data = {
                'deleted': True
            }
        return JsonResponse(data)

class BaseActionAjaxView(View):
    def get(self, request):
        pk = self.request.GET.get('id', None)
        if self.model:
            obj = self.model.object.get(pk=pk)
        data = {
            'object':obj
        }
        return JsonResponse(data)

class BaseAddObjectAjaxView(View):
    def get(self, request):
        pk = self.request.GET.get('id', None)
        fk_pk = self.request.GET.get('fk', None)
        if self.model:
            obj = self.model.object.get(pk=pk)
        data = {
            'object':obj
        }
        return JsonResponse(data)

class BaseRemoveObjectAjaxView(View):
    def get(self, request):
        pk = self.request.GET.get('id', None)
        fk_pk = self.request.GET.get('fk', None)
        if self.model:
            obj = self.model.object.get(pk=pk)
        data = {
            'object':obj
        }
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