from datetime import date
from django.core.validators import validate_email as super_validate_email
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.utils import timezone

from django.conf import settings
import logging
import datetime
import uuid
import os
from utils.file_encryptor import FileEncryptor, FileType, AccessClassification
from django.conf import settings
from django.urls import resolve
from django_extensions.management.commands import show_urls
from django.core import management
import pandas as pd
import json
from django.core.mail import send_mail as native_send_mail

logger = logging.getLogger(__name__)

def public_upload(instance, filename):
    filename, extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    prefix = str(uuid.uuid4().hex)
    return f"{prefix}_{timestamp}{extension}"

def internal_upload(instance, filename, file_type=FileType.UPLOAD, access_classification=AccessClassification.INTERNAL):
    filename = FileEncryptor.create_filename(
        original_filename=filename,
        owner_pk=instance.updated_by.pk,
        file_type=file_type,
        access_classification=access_classification
    )
    return filename

def confidential_upload(instance, filename):
    filename = FileEncryptor.create_filename(
        original_filename=filename,
        owner_pk=instance.updated_by.pk,
        file_type=FileType.UPLOAD,
        access_classification=AccessClassification.CONFIDENTIAL
    )
    return filename

def restricted_upload(instance, filename):
    filename = FileEncryptor.create_filename(
        original_filename=filename,
        owner_pk=instance.updated_by.pk,
        file_type=FileType.UPLOAD,
        access_classification=AccessClassification.RESTRICTED
    )
    return filename

def calculate_age(bday):
    today = date.today()
    return today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))

def validate_email(email):
    username, domain = email.split('@')
    if settings.DEBUG or (
        settings.ALLOWED_DOMAINS and domain in settings.ALLOWED_DOMAINS
        ):
        return super_validate_email(email)

def preregister_user(email, name=None):
    """Creates a user instance without need to go through any logic or be logged in prior

    Args:
        email (_type_): email
        name (_type_, optional): name. Defaults to None.

    Returns:
        user
    """
    username, domain = email.split('@')
    user, is_created = get_user_model().objects.update_or_create(email=email, username=username, defaults={'name':name})
    logger.info(f"User: {user} is_created: {is_created}")
    return user

def valid_year_choices_w_offset(offset=0):
    return [(r,r) for r in range(1908, datetime.date.today().year+1+offset)]

def current_year():
    return datetime.date.today().year

YN_BOOLEAN_CHOICES = ((False, 'No'), (True, 'Yes'))
TF_BOOLEAN_CHOICES = ((False, 'False'), (True, 'True'))

def get_current_domain(with_protocol=True):
    protocol = ""
    if with_protocol:
        protocol = "https://" if settings.SECURE_SSL_REDIRECT else "http://"
    current_domain = Site.objects.get_current().domain
    return f"{protocol}{current_domain}"

def get_sao_group():
    return Group.objects.get(name=settings.QAO_GROUP_NAME)

def pisa_link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """

    static_url = settings.STATIC_URL                # Typically /static/
    static_root = settings.STATICFILES_DIRS[0]      # To resolve static files path
    media_url = settings.MEDIA_URL                  # Typically /media/
    media_root = settings.MEDIA_ROOT                # To resolve media files path
    internal_media_url = settings.INTERNAL_MEDIA_URL                  # Typically /media/
    internal_media_root = settings.INTERNAL_MEDIA_ROOT                # To resolve media files path
    base_dir = settings.ROOT_DIR                    # Project's base directory

    if uri.startswith(media_url):
        path = os.path.join(media_root, uri.replace(media_url, ""))
    if uri.startswith(internal_media_url):
        path = os.path.join(internal_media_root, uri.replace(internal_media_url, ""))
    elif uri.startswith(static_url):
        path = os.path.join(static_root, uri.replace(static_url, ""))
    else:
        path = os.path.join(base_dir, '../', uri)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (static_url, media_url)
        )
    return path

def get_url_df(
    as_url_list=False, 
    exclude_patterns=["detail", "create", "ajax", "update", "delete", "api", "edit"],
    exclude_modules = ["file_management"],
    ):
    values = []
    with open('/tmp/inspectdb', 'w+') as f:
        values = json.loads(management.call_command('show_urls', format="json", stdout=f))
    def url_name(url):
        try:
            resolver = resolve(url)
            url_name = ":".join(resolver.namespaces + [resolver.url_name])
            return url_name
        except Exception as e:
            return None
    df = pd.DataFrame(values)
    df["module_app"] = df['module'].str.extract("(\w+)\..*")
    df["name_valid"] = df["name"].apply(lambda name: True if url_name==None else not any(substr in name for substr in exclude_patterns))
    df = df.query(f"module_app.isin({settings.LOCAL_APPS}) and name_valid and ~module_app.isin({exclude_modules})")
    if as_url_list:
        return df["url"].to_list()
    return df[["url", "module", "name", "module_app"]]

def send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None, allow_sending_on_debug=False):
    # restricts sending mail on production
    if not settings.DEBUG or allow_sending_on_debug:
        native_send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
    else:
        logger.warning(f"Will not send mail to {recipient_list} due to debug settings")