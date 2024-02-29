from django.test import TestCase
import logging
logger = logging.getLogger(__name__)
from {{cookiecutter.app_location_dot_notation}}.tests.factories import {{cookiecutter.model_name_camel_case}}Factory
# from {{cookiecutter.app_location_dot_notation}}.forms import {{cookiecutter.model_name_camel_case}}Form

class {{cookiecutter.model_name_camel_case}}FormsTestCase(TestCase):

    def setUp(self):
        self.object = {{cookiecutter.model_name_camel_case}}Factory()
        logger.info(f"{self.object} created")

    # def test_form_valid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = {{cookiecutter.model_name_camel_case}}Form(data=data)
    #     self.assertTrue(form.is_valid())

    # def test_form_invalid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = {{cookiecutter.model_name_camel_case}}Form(data=data)
    #     self.assertFalse(form.is_valid())

    # def test_form_save(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = {{cookiecutter.model_name_camel_case}}Form(data=data)
    #     saved_obj = form.save()
    #     pass

    def tearDown(self):
        pass