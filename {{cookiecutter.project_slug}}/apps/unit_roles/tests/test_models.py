from django.test import TestCase
from django.urls import resolve, reverse
from unit_roles.models import UnitRole
from unit_roles.tests.factories import UnitRoleFactory
import logging
logger = logging.getLogger(__name__)

class UnitRoleModelTestCase(TestCase):
    def setUp(self):
        self.object = UnitRoleFactory()
        logger.info(f"{self.object} created")

    def test_case_one(self):
        pass

    def tearDown(self):
        pass
