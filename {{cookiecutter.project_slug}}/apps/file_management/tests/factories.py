from factory.django import DjangoModelFactory, FileField
from factory.fuzzy import FuzzyChoice
from file_management.models import DocumentMetadata
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
from django.contrib.contenttypes.models import ContentType
from users.tests.factories import UserFactory
import re
import random

random.seed(0)

def generate_email(record):
    username = record.contact_name.replace(" ", "").lower()
    return f"{username}@up.edu.ph"

class DocumentMetadataFactory(DjangoModelFactory):
    name = Faker("sentence")
    content_type = LazyAttribute(lambda record: ContentType.objects.get_for_model(record.content_object))
    object_id = LazyAttribute(lambda record: record.content_object.pk)
    updated_by = UserFactory()

    class Meta:
        model = DocumentMetadata
