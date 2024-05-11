from django.test import TestCase
import logging
logger = logging.getLogger(__name__)
from module_management.tests.factories import ModuleManagementFactory
# from module_management.forms import ModuleManagementForm

class ModuleManagementFormsTestCase(TestCase):

    def setUp(self):
        self.object = ModuleManagementFactory()
        logger.info(f"{self.object} created")

    # def test_form_valid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = ModuleManagementForm(data=data)
    #     self.assertTrue(form.is_valid())

    # def test_form_invalid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = ModuleManagementForm(data=data)
    #     self.assertFalse(form.is_valid())

    # def test_form_save(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = ModuleManagementForm(data=data)
    #     saved_obj = form.save()
    #     pass

    def tearDown(self):
        pass