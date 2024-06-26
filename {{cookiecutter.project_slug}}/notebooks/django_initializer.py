# In new *.ipynb document: https://blog.theodo.com/2020/11/django-jupyter-vscode-setup/
# import django_initializer

# A script that's needed to setup django if it's not already running on a server.
# Without this, you won't be able to import django modules
import sys, os, django

# Find the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project base directory to the sys.path
# This means the script will look in the base directory for any module imports
# Therefore you'll be able to import analysis.models etc
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, f"{BASE_DIR}/apps")

# The DJANGO_SETTINGS_MODULE has to be set to allow us to access django imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arcwebsite.settings")

#  Allow queryset filtering asynchronously when running in a Jupyter notebook
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# This is for setting up django
django.setup()
