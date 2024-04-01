from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
import os
import pandas as pd
import random

class Command(BaseCommand):
    help = "Reset migrations files for fresh migration alongside reset_db"

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


    def handle(self, *args, **kwargs):
        self.reset_migrations()
