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
from module_management.models import ModuleManagement
from users.tests.factories import UserFactory
from django.contrib.auth import get_user_model

class ModuleManagementFactory(DjangoModelFactory):
    @sequence
    def name(n):
        return f"Module {n}"

    @post_generation
    def post_save_method(self, create, extracted, **kwargs):
        pass

    class Meta:
        model = ModuleManagement
