from django.test import TestCase
import logging
logger = logging.getLogger(__name__)
from guidelines.tests.factories import GuidelineFactory
# from guidelines.forms import GuidelineForm

class GuidelineFormsTestCase(TestCase):

    def setUp(self):
        self.object = GuidelineFactory()
        logger.info(f"{self.object} created")

    # def test_form_valid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = GuidelineForm(data=data)
    #     self.assertTrue(form.is_valid())

    # def test_form_invalid(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = GuidelineForm(data=data)
    #     self.assertFalse(form.is_valid())

    # def test_form_save(self):
    #     data = {'title': self.obj.title, 'body': self.obj.body,}
    #     form = GuidelineForm(data=data)
    #     saved_obj = form.save()
    #     pass

    def tearDown(self):
        pass