from django.shortcuts import render
from module_management.models import NavItem, AccessClassification
from utils.base_views.ajax.views import (
	BaseListAjaxView,
	BaseCreateAjaxView,
	BaseDetailAjaxView,
	BaseUpdateAjaxView,
	BaseDeleteAjaxView,
)
from django.template.loader import render_to_string
from django.views.generic import View
from django.http import JsonResponse
from django.urls import reverse
import logging
logger = logging.getLogger(__name__)


# Create your views here.

class ModuleManagementListAjaxView(BaseListAjaxView):
	model = NavItem
	column_defs = [
		{'name':'label'},
		{'name':'href'},
		{'name':'header'},
		{'name':'icon'},
	]
	initial_order=[["label", "asc"]]

class SidebarAjaxView(View):
	model = NavItem

	def _sort_headers(self, headers):
		if "HOME" in headers:
			headers.remove("HOME")
			headers.insert(0, "HOME")
		if "SETTINGS" in headers:
			headers.remove("SETTINGS")
			headers.insert(len(headers), "SETTINGS")
		return headers


	def get(self, *args, **kwargs):
		query=self.request.GET.get("query")
		items = []
		qs = NavItem.objects.filter(label__icontains=query).exclude(classification=AccessClassification.PUBLIC)
		if not(self.request.user.is_superuser or self.request.user.is_staff):
			qs = qs.filter(classification=AccessClassification.INTERNAL) | qs.filter(classification=AccessClassification.CONFIDENTIAL, groups__user=self.request.user)
		headers = list(qs.distinct("header").values_list("header", flat=True))
		for header in self._sort_headers(headers):
			items.append(render_to_string("detail_wrapper/nav_item_head.html", {'header':header}))
			for sidebar_item in qs.filter(header=header):
				items.append(sidebar_item.as_nav_link)
		#append logout
		items.append(render_to_string("detail_wrapper/nav_item_head.html", {'header':"LOGOUT"}))
		items.append(render_to_string("detail_wrapper/nav_link.html", {'object':{'href':reverse("account_logout"), 'icon':'mdi-logout', 'label':'logout'}}))
		return JsonResponse({'html':"".join(items)})