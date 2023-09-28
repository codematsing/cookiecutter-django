from django.urls import path, include
from file_management.views import pdf_view, download

app_name = "file_management"

urlpatterns = [
    path("pdf/", pdf_view, name="pdf"),
    path("download/", download, name="download"),
    path("ajax/", include('file_management.ajax.urls', 'ajax')),
]