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
    lazy_attribute
)
from django.contrib.auth import get_user_model
from posts.models import Post
from random import randint, sample

class PostFactory(DjangoModelFactory):
    title = Faker("sentence")
    body = Faker("paragraph")
    is_published = Iterator([True, False])

    @lazy_attribute
    def updated_by(self):
        user = get_user_model().objects.filter(groups__isnull=False).first()
        return user


    class Meta:
        model = Post