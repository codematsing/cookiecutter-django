from django.test import TestCase
import logging
logger = logging.getLogger(__name__)
from {{cookiecutter.app_location}}.tests.factories import {{cookiecutter.snake_case_model_name}}Factory
# from {{cookiecutter.app_location}}.forms import {{cookiecutter.snake_case_model_name}}Form

class {{cookiecutter.snake_case_model_name}}FormsTestCase(TestCase):

    def setUp(self):
        self.object = {{cookiecutter.snake_case_model_name}}Factory()
        logger.info(f"{self.object} created")

    # def test_form_valid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = {{cookiecutter.snake_case_model_name}}Form(data=data)
    #     self.assertTrue(form.is_valid())

    # def test_form_invalid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = {{cookiecutter.snake_case_model_name}}Form(data=data)
    #     self.assertFalse(form.is_valid())

    # def test_form_save(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = {{cookiecutter.snake_case_model_name}}Form(data=data)
    #     saved_obj = form.save()
    #     pass

    def tearDown(self):
        pass