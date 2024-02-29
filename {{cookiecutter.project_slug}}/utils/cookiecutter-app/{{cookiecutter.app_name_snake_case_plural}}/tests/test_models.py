from django.test import TestCase
from django.urls import resolve, reverse
from {{cookiecutter.app_location_dot_notation}}.models import {{cookiecutter.model_name_camel_case}}
from {{cookiecutter.app_location_dot_notation}}.tests.factories import {{cookiecutter.model_name_camel_case}}Factory
import logging
logger = logging.getLogger(__name__)

class {{cookiecutter.model_name_camel_case}}ModelTestCase(TestCase):
    def setUp(self):
        self.object = {{cookiecutter.model_name_camel_case}}Factory()
        logger.info(f"{self.object} created")

    def test_case_one(self):
        pass

    def tearDown(self):
        pass
