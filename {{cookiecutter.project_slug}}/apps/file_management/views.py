from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from file_management.models import DocumentSubmission, DocumentMetadata
from django.http import HttpResponse, Http404
from django.conf import settings
from django.http import FileResponse
from utils.file_encryptor import FileEncryptor, AccessClassification
from django.http import FileResponse, Http404, HttpResponse
from utils.base_views.admin_views import AdminCreateFormCollectionView
from file_management.forms import DocumentSubmissionFormset

import os

import logging

logger = logging.getLogger(__name__)

def serve_temp_media_view(request, file, token=None):
    full_path = os.path.join(settings.INTERNAL_MEDIA_ROOT, "upload_temp", file)
    if os.path.exists(full_path) and request.user.is_authenticated:
        return FileResponse(open(full_path, "rb"))
    return Http404

def serve_public_media_view(request, file, token=None):
    full_path = os.path.join(settings.MEDIA_ROOT, file)
    if os.path.exists(full_path):
        return FileResponse(open(full_path, "rb"))
    raise Http404


def serve_internal_media_view(request, file, token=None):
    access_classification = FileEncryptor(file).access_classification
    token = FileEncryptor(file).token
    owner_pk = FileEncryptor(file).owner_pk
    filepath = os.path.join(settings.INTERNAL_MEDIA_ROOT, file)

    user = request.user
    has_internal_permission = (
        access_classification == AccessClassification.INTERNAL and user.is_authenticated
    )
    has_confidential_permission = (
        access_classification == AccessClassification.CONFIDENTIAL
        and user.is_authenticated
        and (owner_pk==request.user.pk or user.is_sao)
    )
    has_restricted_permission = (
        access_classification == AccessClassification.RESTRICTED
        and user.is_authenticated
        and (owner_pk==request.user.pk)
    )

    has_token = False
    try:
        document = DocumentSubmission.objects.filter(object_token__startswith=token).first()
        has_token = token==document.get_access_token_for_user(request.user)
    except Exception as e:
        pass

    if has_internal_permission or has_confidential_permission or has_restricted_permission or user.is_superuser or has_token:
        return FileResponse(open(filepath, "rb"))
    logger.warning(f"{request.user} does not have access to view {file}")
    raise Http404

class DocumentSubmissionFormsetView(AdminCreateFormCollectionView):
    model = DocumentSubmission
    collection_class = DocumentSubmissionFormset

    def get_form_collection(self):
        form_collection = super().get_form_collection()
        user_special_filter = DocumentMetadata.objects.filter(for_scholarships__scholars__scholar=self.request.user) | DocumentMetadata.objects.filter(for_scholarships__applications__applicant=self.request.user)
        metadata_filter = DocumentMetadata.objects.filter(require_for_tags__name__in=[
            "Student Profile",
            "Academic Profile",
        ])
        form_collection.get_field('0.document_form.metadata').queryset = metadata_filter | user_special_filter
        return form_collection

    def get_success_message(self, cleaned_data):
        return f"{self.request.user} has successfully upload document/s"

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
