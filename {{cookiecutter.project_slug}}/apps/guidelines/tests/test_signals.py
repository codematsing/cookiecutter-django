from django.test import TestCase
from guidelines.models import Guideline
from guidelines.tests.factories import GuidelineFactory
import logging
logger = logging.getLogger(__name__)

class GuidelineSignalTestCase(TestCase):

    def setUp(self):
        self.object = GuidelineFactory()
        logger.info(f"{self.object} created")

    def test_case_one(self):
        pass

    def tearDown(self):
        pass