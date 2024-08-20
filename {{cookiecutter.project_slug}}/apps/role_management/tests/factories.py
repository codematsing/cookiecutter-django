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
from role_management.models import Role
from users.tests.factories import UserFactory
from django.contrib.auth import get_user_model

class RoleFactory(DjangoModelFactory):
    @sequence
    def name(n):
        return f"Role {n}"

    @post_generation
    def post_save_method(self, create, extracted, **kwargs):
        pass

    class Meta:
        model = Role
