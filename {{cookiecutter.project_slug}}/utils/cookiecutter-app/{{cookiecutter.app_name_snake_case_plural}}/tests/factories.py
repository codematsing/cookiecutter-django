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
    LazyAttribute,
)
from random import randint, sample
from {{cookiecutter.app_location_dot_notation}}.models import {{cookiecutter.model_name_camel_case}}
from users.tests.factories import UserFactory
from django.contrib.auth import get_user_model

class {{cookiecutter.model_name_camel_case}}Factory(DjangoModelFactory):
    name = Faker("name")
    updated_by = get_user_model().objects.get_or_create(username="updated_by", email="updated_by@example.com")[0]

    class Meta:
        model = {{cookiecutter.model_name_camel_case}}
