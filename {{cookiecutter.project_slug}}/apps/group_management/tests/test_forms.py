from django.test import TestCase
import logging
logger = logging.getLogger(__name__)
from group_management.tests.factories import GroupManagementFactory
# from group_management.forms import GroupManagementForm

class GroupManagementFormsTestCase(TestCase):

    def setUp(self):
        self.object = GroupManagementFactory()
        logger.info(f"{self.object} created")

    # def test_form_valid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = GroupManagementForm(data=data)
    #     self.assertTrue(form.is_valid())

    # def test_form_invalid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = GroupManagementForm(data=data)
    #     self.assertFalse(form.is_valid())

    # def test_form_save(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = GroupManagementForm(data=data)
    #     saved_obj = form.save()
    #     pass

    def tearDown(self):
        pass