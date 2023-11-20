from django.test import TestCase
from django.urls import resolve, reverse
from posts.models import Post
from posts.tests.factories import PostFactory
import logging
logger = logging.getLogger(__name__)

class PostModelTestCase(TestCase):
    def setUp(self):
        self.object = PostFactory()
        logger.info(f"{self.object} created")

    def test_case_one(self):
        pass

    def tearDown(self):
        pass
