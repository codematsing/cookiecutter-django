from django.test import TestCase
from faqs.models import FaqItem
from faqs.tests.factories import FaqItemFactory
import logging
logger = logging.getLogger(__name__)

class FaqItemSignalTestCase(TestCase):

    def setUp(self):
        self.object = FaqItemFactory()
        logger.info(f"{self.object} created")

    def test_case_one(self):
        pass

    def tearDown(self):
        pass