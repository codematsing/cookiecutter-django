from django.urls import path, include
from file_management.views import pdf_view, download, DocumentSubmissionFormsetView

app_name = "file_management"

urlpatterns = [
    path("pdf/", pdf_view, name="pdf"),
    path("download/", download, name="download"),
    path("documents/add", DocumentSubmissionFormsetView.as_view(), name='add_document'),
    path("ajax/", include('file_management.ajax.urls', 'ajax')),
]