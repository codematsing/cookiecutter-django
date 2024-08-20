from django.test import TestCase
import logging
logger = logging.getLogger(__name__)
from unit_roles.tests.factories import UnitRoleFactory
# from unit_roles.forms import UnitRoleForm

class UnitRoleFormsTestCase(TestCase):

    def setUp(self):
        self.object = UnitRoleFactory()
        logger.info(f"{self.object} created")

    # def test_form_valid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = UnitRoleForm(data=data)
    #     self.assertTrue(form.is_valid())

    # def test_form_invalid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = UnitRoleForm(data=data)
    #     self.assertFalse(form.is_valid())

    # def test_form_save(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = UnitRoleForm(data=data)
    #     saved_obj = form.save()
    #     pass

    def tearDown(self):
        pass