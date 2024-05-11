from django.test import TestCase
from django.urls import resolve, reverse
from group_management.models import GroupManagement
from group_management.tests.factories import GroupManagementFactory
import logging
logger = logging.getLogger(__name__)

class GroupManagementModelTestCase(TestCase):
    def setUp(self):
        self.object = GroupManagementFactory()
        logger.info(f"{self.object} created")

    def test_case_one(self):
        pass

    def tearDown(self):
        pass
