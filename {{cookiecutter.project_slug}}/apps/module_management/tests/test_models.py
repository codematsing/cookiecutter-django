from django.test import TestCase
from django.urls import resolve, reverse
from module_management.models import ModuleManagement
from module_management.tests.factories import ModuleManagementFactory
import logging
logger = logging.getLogger(__name__)

class ModuleManagementModelTestCase(TestCase):
    def setUp(self):
        self.object = ModuleManagementFactory()
        logger.info(f"{self.object} created")

    def test_case_one(self):
        pass

    def tearDown(self):
        pass
