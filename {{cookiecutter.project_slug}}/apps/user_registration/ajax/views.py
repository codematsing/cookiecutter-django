from django.shortcuts import render
from django.template.loader import render_to_string

from user_registration.models import Registration

from utils.base_views.ajax.views import (
    BaseListAjaxView,
    BaseCreateAjaxView,
    BaseDetailAjaxView,
    BaseUpdateAjaxView,
    BaseDeleteAjaxView,
    BaseActionAjaxView,
    BaseAddObjectAjaxView,
    BaseRemoveObjectAjaxView,
    BaseActionObjectAjaxView,
)

# Create your views here.

class RegistrationListAjaxView(BaseListAjaxView):
    model = Registration
    column_defs = [
        {'name':'pk', 'visible':False},
        {'name':'last_name'},
        {'name':'first_name'},
        {'name':'email'},
        {'name':'approve', 'title':'Approve', 'searchable':False},
        {'name':'reject', 'title':'Reject', 'searchable':False},
    ]

    def get_initial_queryset(self, request):
        qs = self.model.objects.filter(is_approved=False)
        qs = self.filter_qs_from_params(request, qs)
        qs = self.filter_qs_from_data(request, qs)
        return qs

    def customize_row(self, row, obj):
        row['approve'] = f"""
            <a href="{obj.get_approve_url()}">
            <i class="mdi mdi-account-check mdi-24px text-success" title="Approve"></i>
            </a>
            """
        row['reject'] = f"""
            <a href="{obj.get_reject_url()}">
            <i class="mdi mdi-account-off mdi-24px text-primary" title="Reject"></i>
            </a>
            """
        return

class RegistrationCreateAjaxView(BaseCreateAjaxView):
    model = Registration

class RegistrationDetailAjaxView(BaseDetailAjaxView):
    model = Registration

class RegistrationUpdateAjaxView(BaseUpdateAjaxView):
    model = Registration

class RegistrationDeleteAjaxView(BaseDeleteAjaxView):
    model = Registration
