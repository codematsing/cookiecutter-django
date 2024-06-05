from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from file_management.models import DocumentSubmission
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import redirect
from utils.file_encryptor import FileEncryptor, AccessClassification
from django.views import static
import posixpath
from django.contrib.staticfiles import finders

import mimetypes
import posixpath
from pathlib import Path

from django.http import FileResponse, Http404, HttpResponse, HttpResponseNotModified
from django.template import Context, Engine, TemplateDoesNotExist, loader
from django.utils._os import safe_join
from django.utils.http import http_date, parse_http_date
from django.views.static import directory_index, was_modified_since

import os

import logging

logger = logging.getLogger(__name__)

def serve_temp_media_view(request, file):
    full_path = os.path.join(settings.INTERNAL_MEDIA_ROOT, "upload_temp", file)
    if os.path.exists(full_path) and request.user.is_authenticated:
        return FileResponse(open(full_path, "rb"))
    return Http404

def serve_public_media_view(request, file):
    full_path = os.path.join(settings.MEDIA_ROOT, file)
    if os.path.exists(full_path):
        return FileResponse(open(full_path, "rb"))
    raise Http404


def serve_internal_media_view(request, file):
    owner = FileEncryptor(file).owner
    access_classification = FileEncryptor(file).access_classification
    user = request.user
    filepath = os.path.join(settings.INTERNAL_MEDIA_ROOT, file)
    has_internal_permission = (
        access_classification == AccessClassification.INTERNAL and user.is_authenticated
    )
    has_confidential_permission = (
        access_classification == AccessClassification.CONFIDENTIAL
        and user.is_authenticated
        and (owner == user or user.is_sao)
    )
    has_restricted_permission = (
        access_classification == AccessClassification.RESTRICTED
        and user.is_authenticated
        and (owner == user)
    )
    logger.info(has_internal_permission)
    logger.info(has_confidential_permission)
    logger.info(has_restricted_permission)
    if has_internal_permission or has_confidential_permission or has_restricted_permission or user.is_superuser:
        return FileResponse(open(filepath, "rb"))
    raise Http404

@xframe_options_exempt
def pdf_view(request, *args, **kwargs):
    """
    Use of pdfjs as document viewer to control if user can download files
    """
    # NOTE: I think this is not needed anymore, let the view handle accessibility of files
    # filename = request.GET['file']
    # logger.info(f'Filename GET: {filename}')
    # filename = filename.replace('/media/', '')
    # if submission := DocumentSubmission.objects.filter(attachment__icontains=filename).last():
    # 	if not request.user.is_anonymous and request.user.is_sao or request.user==submission.updated_by:
    # 		return render(request, "pdf/viewer.html", context={'is_downloadable': True})
    # 	else:
    # 		return HttpResponseForbidden()
    # else:
    # 	# Workaround for Auto generated PDFs
    return render(request, "pdf/viewer.html", context={"is_downloadable": True})


def download(request, *args, **kwargs):
    filename = request.GET["file"]
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    submission = DocumentSubmission.objects.filter(
        attachment__icontains=filename
    ).last()
    if request.user.has_perm("view_documentsubmission", submission) and os.path.exists(
        file_path
    ):
        with open(file_path, "rb") as fh:
            response = HttpResponse(submission, content_type="application/pdf")
            response["Content-Disposition"] = (
                f'attachment; filename="{submission}_uploadedby_{submission.updated_by.username}"'
            )
            return response
    raise Http404
