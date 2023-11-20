from django.test import TestCase
from django.urls import resolve, reverse
from {{cookiecutter.app_location}}.models import {{cookiecutter.camel_case_model_name}}
from {{cookiecutter.app_location}}.tests.factories import {{cookiecutter.camel_case_model_name}}Factory
import logging
logger = logging.getLogger(__name__)

class {{cookiecutter.camel_case_model_name}}ModelTestCase(TestCase):
    def setUp(self):
        self.object = {{cookiecutter.camel_case_model_name}}Factory()
        logger.info(f"{self.object} created")

    def test_case_one(self):
        pass

    def tearDown(self):
        pass
