from django.shortcuts import render
from file_management.models import DocumentMetadata, DocumentSubmission
from utils.base_views.ajax.views import (
	BaseListAjaxView,
	BaseCreateAjaxView,
	BaseDetailAjaxView,
	BaseUpdateAjaxView,
	BaseDeleteAjaxView,
)

# Create your views here.

class DocumentMetadataListAjaxView(BaseListAjaxView):
	model = DocumentMetadata
	column_defs = [
		{'name':'pk', 'visible':False},
		{'name':'name', 'searchable':False},
	]

class DocumentSubmissionListAjaxView(BaseListAjaxView):
	model = DocumentSubmission