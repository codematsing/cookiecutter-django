from typing import Any, Dict, List
from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView
from utils.base_views.views import BaseWAjaxDatatableMixin

# Create your views here.
class DashboardView(BaseWAjaxDatatableMixin, TemplateView):
    template_name = "commons/dashboard.html"