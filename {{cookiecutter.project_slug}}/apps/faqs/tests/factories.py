from factory.django import DjangoModelFactory, FileField
from factory.fuzzy import FuzzyChoice
from factory import (
    SubFactory,
    Faker,
    PostGenerationMethodCall,
    Sequence,
    RelatedFactory,
    Iterator,
    post_generation,
    lazy_attribute,
    sequence,
)
from random import randint, sample
from faqs.models import FaqItem
from sikap.users.tests.factories import UserFactory
from django.contrib.auth import get_user_model

class FaqItemFactory(DjangoModelFactory):
    name = Faker("name")

    @sequence
    def name(self, n):
        return f"{self}{n}"

    @post_generation
    def post_save_method(self, create, extracted, **kwargs):
        pass

    class Meta:
        model = FaqItem
