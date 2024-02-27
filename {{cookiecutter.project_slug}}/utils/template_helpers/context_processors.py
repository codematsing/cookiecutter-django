from django.conf import settings
from utils.lambdas import get_current_domain

def current_domain(request):
    return {'current_domain' : get_current_domain()}