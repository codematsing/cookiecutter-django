from posts.models import Post
from utils.base_views.ajax.views import (
	BaseListAjaxView,
)
from auditlog.models import LogEntry
import logging
from urllib.parse import parse_qs
from django.http import Http404
from django.urls import resolve
from django.contrib.contenttypes.models import ContentType
from utils.base_models.models import AbstractAuditedModel
from django.contrib.humanize.templatetags.humanize import naturalday
import json
import uuid
import re
logger = logging.getLogger(__name__)

# Create your views here.

class HistoryListAjaxView(BaseListAjaxView):
	model = LogEntry
	show_date_filters = True
	column_defs = [
		{'name':'pk', 'visible':False},
		{'name':'timestamp', 'title':'Timestamp', 'searchable':False},
		{'name':'actor', 'title':'Updated by', 'foreign_field':'actor__username'},
		{'name':'additional_data', 'title':'Remarks'},
	]
	initial_order=[["timestamp", "desc"]]

	def get_object_model(self):
		referrer = self.request.META.get("HTTP_REFERRER", self.request.headers['Referer'])
		referrer = re.sub(r"(https?://[^\/]+)(.*)", r"\2", referrer)
		resolver_match = resolve(referrer)
		model = getattr(resolver_match.func.view_class, "model")
		return model

	def get_object(self):
		object_model = self.get_object_model()
		token = self.request.REQUEST.get('token', None)
		pk, access_token = token.split("-")
		_object: AbstractAuditedModel = object_model.objects.get(pk=pk)
		logger.info(_object.get_access_token_for_user(self.request.user))
		logger.info(access_token)
		if access_token == _object.get_access_token_for_user(self.request.user):
			return _object
		return None

	# object column defs and customization are obtained from model classmethod setups
	def get_column_defs(self, request):
		return self.get_object_model().get_history_column_defs()

	def get_initial_queryset(self, request):
		obj = self.get_object()
		return obj.history.all()

	def customize_row(self, row, obj):
		if obj.actor==None:
			row['actor'] = '<i>system generated</i>'
		return self.get_object_model().get_history_customize_row(row, obj)