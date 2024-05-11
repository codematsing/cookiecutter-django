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
from group_management.models import GroupManagement
from users.tests.factories import UserFactory
from django.contrib.auth import get_user_model

class GroupManagementFactory(DjangoModelFactory):
    @sequence
    def name(self, n):
        return f"{self}{n}"

    @lazy_attribute
    def updated_by(self):
        return get_user_model().objects.get_or_create(username="updated_by", email="updated_by@example.com")[0]

    @post_generation
    def post_save_method(self, create, extracted, **kwargs):
        pass

    class Meta:
        model = GroupManagement
