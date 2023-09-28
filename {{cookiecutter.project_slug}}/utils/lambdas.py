from datetime import date
from django.core.validators import validate_email as super_validate_email
from django.conf import settings
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

def calculate_age(bday):
    today = date.today()
    return today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))

def validate_email(email):
    username, domain = email.split('@')
    if settings.DEBUG or (
        settings.ALLOWED_DOMAINS and domain in settings.ALLOWED_DOMAINS
        ):
        return super_validate_email(email)

def preregister_email(email):
    username, domain = email.split('@')
    user, is_created = get_user_model().objects.get_or_create(email=email, username=username)
    logger.info(f"User: {user} is_created: {is_created}")
    return user