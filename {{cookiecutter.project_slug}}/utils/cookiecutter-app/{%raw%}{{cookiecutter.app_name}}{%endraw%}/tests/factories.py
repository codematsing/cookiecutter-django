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
from {{cookiecutter.app_name}}.models import {{cookiecutter.snake_case_model_name}}
from {{cookiecutter.project_slug}}.users.tests.factories import UserFactory

class {{cookiecutter.snake_case_model_name}}Factory(DjangoModelFactory):
    updated_by = SubFactory(UserFactory)

    class Meta:
        model = {{cookiecutter.snake_case_model_name}}
