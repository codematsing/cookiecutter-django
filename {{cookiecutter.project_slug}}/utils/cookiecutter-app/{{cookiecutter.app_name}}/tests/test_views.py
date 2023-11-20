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
from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory
from {{cookiecutter.app_location}}.tests.factories import {{cookiecutter.camel_case_model_name}}Factory
from {{cookiecutter.app_location}}.views import (
    {{cookiecutter.camel_case_model_name}}ListView,
    {{cookiecutter.camel_case_model_name}}DetailView,
    {{cookiecutter.camel_case_model_name}}UpdateView,
    {{cookiecutter.camel_case_model_name}}DeleteView,
)
import logging
logger = logging.getLogger(__name__)

class {{cookiecutter.camel_case_model_name}}ViewTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.object = {{cookiecutter.camel_case_model_name}}Factory(updated_by=self.user)
        logger.info(f"{self.object} created")

    # def test_list_view(self):
    #     self.client.login(username=self.user.username, password=self.user.password)
    #     url_name = '{{cookiecutter.app_name}}:list'
    #     url = reverse(url_name)
    #     response = self.client.get(url)
    #     self.assertTemplateUsed(response, 'pages/list.html')
    #     self.assertEqual(response.context['objects'], self.user.get_{{cookiecutter.model_name}})

    # def test_detail_view(self):
    #     self.client.login(username=self.user.username, password=self.user.password)
    #     url_name = '{{cookiecutter.app_name}}:detail'
    #     url = reverse(url_name, kwargs={'pk': self.mymodel.pk})
    #     response = self.client.get(url)
    #     self.assertTemplateUsed(response, 'pages/detail.html')
    #     self.assertEqual(response.context['object'], self.user.get_{{cookiecutter.model_name}})

    def tearDown(self):
        pass