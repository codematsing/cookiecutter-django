from django.test import TestCase
from unit_roles.models import UnitRole
from unit_roles.tests.factories import UnitRoleFactory
import logging
logger = logging.getLogger(__name__)

class UnitRoleSignalTestCase(TestCase):

    def setUp(self):
        self.object = UnitRoleFactory()
        logger.info(f"{self.object} created")

    def test_case_one(self):
        pass

    def tearDown(self):
        pass