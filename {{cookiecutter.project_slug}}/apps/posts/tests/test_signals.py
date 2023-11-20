from django.test import TestCase
from posts.models import Post
from posts.tests.factories import PostFactory
import logging
logger = logging.getLogger(__name__)

class PostSignalTestCase(TestCase):

    def setUp(self):
        self.object = PostFactory()
        logger.info(f"{self.object} created")

    def test_case_one(self):
        pass

    def tearDown(self):
        pass