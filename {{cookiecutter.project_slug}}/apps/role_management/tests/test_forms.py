from django.test import TestCase
import logging
logger = logging.getLogger(__name__)
from role_management.tests.factories import RoleFactory
# from role_management.forms import RoleForm

class RoleFormsTestCase(TestCase):

    def setUp(self):
        self.object = RoleFactory()
        logger.info(f"{self.object} created")

    # def test_form_valid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = RoleForm(data=data)
    #     self.assertTrue(form.is_valid())

    # def test_form_invalid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = RoleForm(data=data)
    #     self.assertFalse(form.is_valid())

    # def test_form_save(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = RoleForm(data=data)
    #     saved_obj = form.save()
    #     pass

    def tearDown(self):
        pass