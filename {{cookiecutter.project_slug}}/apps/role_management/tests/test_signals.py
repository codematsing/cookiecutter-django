from django.test import TestCase
from role_management.models import Role
from role_management.tests.factories import RoleFactory
import logging
logger = logging.getLogger(__name__)

class RoleSignalTestCase(TestCase):

    def setUp(self):
        self.object = RoleFactory()
        logger.info(f"{self.object} created")

    def test_case_one(self):
        pass

    def tearDown(self):
        pass