from django.views.generic import View
from ajax_datatable.views import AjaxDatatableView
from django.http import JsonResponse
from django.template.loader import render_to_string

import logging
logger = logging.getLogger(__name__)

class BaseListAjaxView(AjaxDatatableView):
    # show_column_filters=False
    column_defs = [
        {'name':'pk', 'visible':False},
        {'name':'action'},
    ]
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