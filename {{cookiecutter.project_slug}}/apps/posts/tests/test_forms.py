from django.test import TestCase
import logging
logger = logging.getLogger(__name__)
from posts.tests.factories import PostFactory
# from posts.forms import PostForm

class PostFormsTestCase(TestCase):

    def setUp(self):
        self.object = PostFactory()
        logger.info(f"{self.object} created")

    # def test_form_valid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = PostForm(data=data)
    #     self.assertTrue(form.is_valid())

    # def test_form_invalid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = PostForm(data=data)
    #     self.assertFalse(form.is_valid())

    # def test_form_save(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = PostForm(data=data)
    #     saved_obj = form.save()
    #     pass

    def tearDown(self):
        pass