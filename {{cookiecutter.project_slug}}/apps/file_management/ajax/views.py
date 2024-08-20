from django.shortcuts import render
from file_management.models import DocumentMetadata, DocumentSubmission
from django.core.exceptions import PermissionDenied
from utils.base_views.ajax.views import (
	BaseListAjaxView,
	BaseCreateAjaxView,
	BaseDetailAjaxView,
	BaseUpdateAjaxView,
	BaseDeleteAjaxView,
)
from django.template.loader import render_to_string
import logging
logger = logging.getLogger(__name__)

# Create your views here.

class DocumentMetadataListAjaxView(BaseListAjaxView):
	model = DocumentMetadata
	column_defs = [
		{'name':'pk', 'visible':False},
		{'name':'name', 'searchable':False},
		{'name':'require_for_tags', 'm2m_foreign_field': 'require_for_tags__name','searchable':False},
	]

class DocumentSubmissionListAjaxView(BaseListAjaxView):
	model = DocumentSubmission
	column_defs = [
		{'name':'pk', 'visible':False},
		{'name':'document', 'title':'Document', 'foreign_field':'metadata__name'},
		{'name':'updated_at'},
		{'name':'action'},
	]

	def get_initial_queryset(self, request):
		qs =  super().get_initial_queryset(request)
		logger.info(self.request.REQUEST.get('query'))
		if self.request.user.is_sao:
			return qs
		elif self.request.REQUEST.get('query'):
			return qs.filter(academic_profile__user=self.request.user)
		raise PermissionDenied

	def test_func(self):
		return self.request.user.is_authenticated

	def customize_row(self, row, obj):
		row['action'] = render_to_string('file_management/submissions_action_column.html', {'record':obj, 'has_update_permission':self.get_update_permission()}) 
		return