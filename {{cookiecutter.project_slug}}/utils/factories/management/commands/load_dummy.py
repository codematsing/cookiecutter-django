from django.core.management.base import BaseCommand
from utils.factories.factories import(
)
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "create dummy data"

    def handle(self, *args, **kwargs):
        admin_user = get_user_model().objects.get_or_create(
            username='admin', email='admin@example.com', is_superuser=True)[0]
        admin_user.set_password('qwer1234')
        admin_user.save()