from django.urls import resolve, reverse
from django.test import TestCase
from django.test import Client
from {{cookiecutter.project_slug}}.users.tests.factories import UserFactory
from {{cookiecutter.app_location}}.tests.factories import {{cookiecutter.snake_case_model_name}}Factory
import logging
logger = logging.getLogger(__name__)

class {{cookiecutter.snake_case_model_name}}UrlsTestCase(TestCase):

    def setUp(self):
        self.object = {{cookiecutter.snake_case_model_name}}Factory()
        logger.info(f"{self.object} created")
        self.client = Client()

    # def test_redirect_if_not_logged_in(self):
    #     url_name = 'home'
    #     response = self.client.get(reverse(url_name, kwargs={'pk': self.test_bookinstance1.pk}))
    #     self.assertEqual(response.status_code, 302)

    # def test_forbidden_user(self):
    #     url_name = 'home'
    #     new_user = UserFactory()
    #     login = self.client.login(username=new_user.username, password=new_user.password)
    #     response = self.client.get(reverse(url_name))
    #     self.assertEqual(response.status_code, 403)

    # def test_allowed_user(self):
    #     url_name = 'home'
    #     new_user = UserFactory()
    #     login = self.client.login(username=new_user.username, password=new_user.password)
    #     response = self.client.get(reverse(url_name))
    #     self.assertEqual(response.status_code, 200)

    # def test_not_found(self):
    #     url_name = 'home'
    #     new_user = UserFactory()
    #     login = self.client.login(username=new_user.username, password=new_user.password)
    #     response = self.client.get(reverse(url_name))
    #     self.assertEqual(response.status_code, 404)

    def tearDown(self):
        pass