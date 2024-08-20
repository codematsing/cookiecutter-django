from factory.django import DjangoModelFactory
from factory import (
    Faker,
    Sequence,
    Iterator,
    lazy_attribute
)
from django.contrib.auth import get_user_model
from posts.models import Post
from random import randint, sample
import uuid

class PostFactory(DjangoModelFactory):
    body = Faker("paragraph")

    @lazy_attribute
    def title(self):
        return f"Post Title {Post.objects.count()+1}"

    class Meta:
        model = Post