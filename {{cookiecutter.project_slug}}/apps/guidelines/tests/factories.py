from factory.django import DjangoModelFactory, FileField
from factory.fuzzy import FuzzyChoice
from factory import (
    Faker,
    SubFactory,
    RelatedFactory,
    Iterator,
    sequence, # decorator
    post_generation, #decorator
    lazy_attribute, #decorator
)
from random import randint, sample
from guidelines.models import Guideline
from users.tests.factories import UserFactory
from django.contrib.auth import get_user_model

class GuidelineFactory(DjangoModelFactory):
    @sequence
    def name(n):
        return f"Guideline{n}"

    @post_generation
    def post_save_method(self, create, extracted, **kwargs):
        pass

    class Meta:
        model = Guideline
