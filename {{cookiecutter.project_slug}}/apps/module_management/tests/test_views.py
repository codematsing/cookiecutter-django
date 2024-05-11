import pytest
from django.test import TestCase
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest, HttpResponseRedirect
from django.test import Client, RequestFactory
from django.urls import reverse
from users.tests.factories import UserFactory
from module_management.tests.factories import ModuleManagementFactory
from module_management.views import (
    ModuleManagementListView,
    ModuleManagementDetailView,
    ModuleManagementUpdateView,
    ModuleManagementDeleteView,
)
import logging
logger = logging.getLogger(__name__)

class ModuleManagementViewTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.object = ModuleManagementFactory(updated_by=self.user)
        logger.info(f"{self.object} created")

    # def test_list_view(self):
    #     self.client.login(username=self.user.username, password=self.user.password)
    #     url_name = 'module_management:list'
    #     url = reverse(url_name)
    #     response = self.client.get(url)
    #     self.assertTemplateUsed(response, 'pages/list.html')
    #     self.assertEqual(response.context['objects'], self.user.get_module_management)

    # def test_detail_view(self):
    #     self.client.login(username=self.user.username, password=self.user.password)
    #     url_name = 'module_management:detail'
    #     url = reverse(url_name, kwargs={'pk': self.mymodel.pk})
    #     response = self.client.get(url)
    #     self.assertTemplateUsed(response, 'pages/detail.html')
    #     self.assertEqual(response.context['object'], self.user.get_module_management)

    def tearDown(self):
        pass
