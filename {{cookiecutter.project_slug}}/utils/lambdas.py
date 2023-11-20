from datetime import date
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import validate_email as super_validate_email
from django.utils import timezone
import datetime
import logging
import os
import uuid

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

def valid_year_choices_w_offset(offset=0):
    return [(r,r) for r in range(1908, datetime.date.today().year+1+offset)]

def current_year():
    return datetime.date.today().year

def rename_upload(instance, filename):
    _, extension = os.path.splitext(filename)
    timestamp = instance.updated_at.strftime('%Y%m%d%H%M%S')
    return f"{uuid.uuid4().hex}_timestamp{extension}" 

def image_upload(instance, filename):
    _, extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f"{uuid.uuid4().hex}_timestamp{extension}" 

YN_BOOLEAN_CHOICES = ((False, 'No'), (True, 'Yes'))
TF_BOOLEAN_CHOICES = ((False, 'False'), (True, 'True'))