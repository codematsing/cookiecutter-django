from django.urls import resolve, reverse
from django.test import TestCase
from django.test import Client
from users.tests.factories import UserFactory
from unit_roles.tests.factories import UnitRoleFactory
import logging
logger = logging.getLogger(__name__)

class UnitRoleUrlsTestCase(TestCase):

    def setUp(self):
        self.object = UnitRoleFactory()
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