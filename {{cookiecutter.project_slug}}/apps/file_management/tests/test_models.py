from django.test import TestCase
from file_management.tests.factories import DocumentMetadataFactory, DocumentSubmissionFactory
from utils.permissions import AccessClassification
from sikap.users.tests.factories import UserFactory
import logging
logger = logging.getLogger(__name__)

class ModelTestCase(TestCase):
    def setUp(self):
        self.object = UserFactory()
        self.public_metadata = DocumentMetadataFactory.create(
            access_classification=AccessClassification.PUBLIC,
            content_object=self.object,
            )
        self.internal_metadata = DocumentMetadataFactory.create(
            access_classification=AccessClassification.INTERNAL,
            content_object=self.object,
            )
        self.confidential_metadata = DocumentMetadataFactory.create(
            access_classification=AccessClassification.CONFIDENTIAL,
            content_object=self.object,
            )
        self.restricted_metadata = DocumentMetadataFactory.create(
            access_classification=AccessClassification.RESTRICTED,
            content_object=self.object,
            )

    def test_public_doc_location_is_public(self):
        public_doc = DocumentSubmissionFactory.create(
            metadata=self.public_metadata, 
            content_object=self.object,
        )
        self.assertTrue("/P/" in public_doc.attachment.url)

    def test_internal_doc_location_is_internal(self):
        internal_doc = DocumentSubmissionFactory.create(
            metadata=self.internal_metadata, 
            content_object=self.object,
        )
        self.assertTrue("/I/" in internal_doc.attachment.url)

    def test_confidential_doc_location_is_confidential(self):
        confidential_doc = DocumentSubmissionFactory.create(
            metadata=self.confidential_metadata, 
            content_object=self.object,
        )
        self.assertTrue("/C/" in confidential_doc.attachment.url)

    def test_restricted_doc_location_is_restricted(self):
        restricted_doc = DocumentSubmissionFactory.create(
            metadata=self.restricted_metadata, 
            content_object=self.object,
        )
        self.assertTrue("/R/" in restricted_doc.attachment.url)

    def tearDown(self):
        pass

