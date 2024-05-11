from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from file_management.models import DocumentSubmission
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import redirect
from utils.file_encryptor import FileEncryptor, AccessClassification

import os

import logging

logger = logging.getLogger(__name__)


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
