from django.contrib import admin
from .models import DocumentMetadata, DocumentSubmission

# Register your models here.
admin.site.register(DocumentSubmission)
admin.site.register(DocumentMetadata)