from django.test import TestCase
from group_management.models import GroupManagement
from group_management.tests.factories import GroupManagementFactory
import logging
logger = logging.getLogger(__name__)

class GroupManagementSignalTestCase(TestCase):

    def setUp(self):
        self.object = GroupManagementFactory()
        logger.info(f"{self.object} created")

    def test_case_one(self):
        pass

    def tearDown(self):
        pass