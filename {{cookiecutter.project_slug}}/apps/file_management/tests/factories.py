from factory.django import DjangoModelFactory
from file_management.models import DocumentMetadata, DocumentSubmission
from factory import (
    Faker,
    Iterator,
    post_generation,
    lazy_attribute,
    SubFactory
)

from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from sikap.users.tests.factories import UserFactory
import re
import random
from logging import getLogger
logger = getLogger(__name__)

random.seed(0)

def generate_email(record):
    username = record.contact_name.replace(" ", "").lower()
    return f"{username}@up.edu.ph"

class DocumentMetadataFactory(DjangoModelFactory):
    name = Faker("sentence")
    content_object = SubFactory(UserFactory)

    @lazy_attribute
    def content_type(self):
        logger.info(self.content_object)
        return ContentType.objects.get_for_model(self.content_object)

    @lazy_attribute
    def object_id(self):
        logger.info(self.content_object)
        return self.content_object.pk

    class Meta:
        model = DocumentMetadata

def get_pdf_data(content):
    pdf_content = (
        "%PDF-1.3\n"
        "1 0 obj\n"
        "<< /Type /Catalog /Pages 2 0 R >>\n"
        "endobj\n"
        "2 0 obj\n"
        "<< /Type /Pages /Count 1 /Kids [3 0 R] >>\n"
        "endobj\n"
        "3 0 obj\n"
        "<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> /ProcSet [ /PDF /Text ] >> /MediaBox [ 0 0 612 792 ] /Contents 4 0 R >>\n"
        "endobj\n"
        "4 0 obj\n"
        "<< /Length 49 >>\n"
        "stream\n"
        "BT\n"
        "/F1 12 Tf\n"
        "72 720 Td\n"
        "(" + content + ") Tj\n"
        "ET\n"
        "endstream\n"
        "endobj\n"
        "xref\n"
        "0 5\n"
        "0000000000 65535 f \n"
        "0000000019 00000 n \n"
        "0000000078 00000 n \n"
        "0000000145 00000 n \n"
        "trailer\n"
        "<< /Size 5 /Root 1 0 R >>\n"
        "startxref\n"
        "186\n"
        "%%EOF"
    )
    return pdf_content

class DocumentSubmissionFactory(DjangoModelFactory):
    metadata = Iterator(DocumentMetadata.objects.all())
    content_object = SubFactory(UserFactory)
    owner = SubFactory(UserFactory)

    @post_generation
    def create_file(self, create, extracted, **kwargs):
        if not create:
            return
        # create a ContentFile with a custom name based on my_attribute
        filename = f"doc{self.metadata.documentsubmission_set.count()}.pdf"
        file_content = get_pdf_data(f"{self.content_object} {self.metadata}")
        content_file = ContentFile(file_content, name=filename)
        # set the file field to the ContentFile
        self.attachment.save(filename, content_file, save=True)
        self.save()

    class Meta:
        model = DocumentSubmission
