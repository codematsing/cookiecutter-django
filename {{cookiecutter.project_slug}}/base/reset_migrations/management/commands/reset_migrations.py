from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
import os
import pandas as pd
import random

class Command(BaseCommand):
    help = "Reset migrations files for fresh migration alongside reset_db"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="Forces reset of migrations",
        )

    def reset_migrations(self):
        included_dirs = [os.path.join(settings.ROOT_DIR, _dir) for _dir in ['apps', 'utils']]
        exception_dirs = [
            "base/contrib/sites/migrations",
            "utils/cookiecutter-app",
        ]
        for root_path in (included_dirs):
            for root, dirnames, files in os.walk(root_path):
                if root.endswith("migrations") and not any(root.find(exception)!=-1 for exception in exception_dirs):
                    for f in files:
                        if f != "__init__.py":
                            filepath = os.path.join(root,f)
                            print(f"Removing {filepath}")
                            # os.remove(filepath)


    def handle(self, *args, **options):
        if settings.DEBUG==False and not options['force']:
            print("WARNING: You are in a production environment setting.")
            print("add --force to reset migrations")
            print("PROCEED WITH CAUTION!")
        else:
            self.reset_migrations()