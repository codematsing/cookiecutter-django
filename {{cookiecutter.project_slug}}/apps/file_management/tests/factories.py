from factory.django import DjangoModelFactory, FileField
from factory.fuzzy import FuzzyChoice
from file_management.models import DocumentMetadata, DocumentSubmission
from factory import (
    SubFactory,
    Faker,
    PostGenerationMethodCall,
    Sequence,
    RelatedFactory,
    Iterator,
    post_generation,
    LazyAttribute,
)
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from users.tests.factories import UserFactory
import re
import random

random.seed(0)

def generate_email(record):
    username = record.contact_name.replace(" ", "").lower()
    return f"{username}@up.edu.ph"

class DocumentMetadataFactory(DjangoModelFactory):
    name = Faker("sentence")
    content_type = LazyAttribute(lambda record: ContentType.objects.get_for_model(record.content_object))
    object_id = LazyAttribute(lambda record: record.content_object.pk)
    updated_by = UserFactory()

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

    @post_generation
    def create_file(self, create, extracted, **kwargs):
        if not create:
            return
        # create a ContentFile with a custom name based on my_attribute
        filename = f"doc{self.metadata.documentsubmission_set.count()}.pdf"
        file_content = get_pdf_data(f"{self.content_object} {self.metadata} of {self.updated_by}")
        content_file = ContentFile(file_content, name=filename)
        # set the file field to the ContentFile
        self.attachment.save(filename, content_file, save=True)
        self.save()

    class Meta:
        model = DocumentSubmission
