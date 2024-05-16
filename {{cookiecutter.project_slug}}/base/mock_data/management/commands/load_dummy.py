from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.core import management
from django.conf import settings
from faker import Faker
from random import choices, randint, choice
import os
import pandas as pd
import random

random.seed(0)
Faker.seed(0)

class Command(BaseCommand):
    help = "create dummy data"

    fixture_files = [
        "sidebar.json",
    ]

    def setup_initial_users(self):
        admin_user = get_user_model().objects.get_or_create(
            username="admin",
            email="admin@example.com",
            is_superuser=True,
            is_active=True,
            is_staff=True,
        )[0]
        for user in [admin_user]:
            user.set_password("qwer!@#$")
            user.save()

    def load_fixtures(self):
        for fixture in self.fixture_files:
            fixture_path = os.path.join(settings.BASE_DIR, "fixtures", fixture)
            management.call_command("loaddata", fixture_path)


    def handle(self, *args, **kwargs):
        self.setup_initial_users()
        self.load_fixtures()