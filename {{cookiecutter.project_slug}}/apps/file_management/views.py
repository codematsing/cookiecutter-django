from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from file_management.models import DocumentSubmission
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.conf import settings
import os

import logging
logger = logging.getLogger(__name__)

@xframe_options_exempt
def pdf_view(request, *args, **kwargs):
	"""
		Use of pdfjs as document viewer to control if user can download files
	"""
	filename = request.GET['file']
	filename = filename.replace('/media/', '')
	submission = DocumentSubmission.objects.filter(attachment__icontains=filename).last()
	if request.user.has_perm('view_documentsubmission', submission):
		return render(request, "pdf/viewer.html", context={'is_downloadable': True})
	return HttpResponseForbidden()

def download(request, *args, **kwargs):
	filename = request.GET['file']
	file_path = os.path.join(settings.MEDIA_ROOT, filename)
	submission = DocumentSubmission.objects.filter(attachment__icontains=filename).last()
	if request.user.has_perm('view_documentsubmission', submission) and os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(submission, content_type='application/pdf')
			response['Content-Disposition'] = f'attachment; filename="{submission}_uploadedby_{submission.updated_by.username}"'
			return response
	raise Http404