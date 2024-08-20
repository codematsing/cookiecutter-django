from datetime import date
from django.core.validators import validate_email as super_validate_email
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.utils import timezone
import logging
import datetime
import uuid
import os
from utils.file_encryptor import FileEncryptor, FileType, AccessClassification
import json
from django.core import management
import pandas as pd
from django.core.mail import EmailMultiAlternatives, get_connection
from django.utils.html import strip_tags
import inspect

logger = logging.getLogger(__name__)

def public_upload(instance, filename):
	filename, extension = os.path.splitext(filename)
	timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
	prefix = str(uuid.uuid4().hex)
	return f"{prefix}_{timestamp}{extension}"

def internal_upload(instance, filename, file_type=FileType.UPLOAD, access_classification=AccessClassification.INTERNAL):
	filename = FileEncryptor.create_filename(
		original_filename=filename,
		token=instance.first_object_token_chars,
		file_type=FileType.UPLOAD,
		owner_pk=instance.owner.pk,
		access_classification=access_classification
	)
	return filename

def confidential_upload(instance, filename):
	filename = FileEncryptor.create_filename(
		original_filename=filename,
		token=instance.first_object_token_chars,
		file_type=FileType.UPLOAD,
		owner_pk=instance.owner.pk,
		access_classification=AccessClassification.CONFIDENTIAL
	)
	return filename

def restricted_upload(instance, filename):
	filename = FileEncryptor.create_filename(
		original_filename=filename,
		token=instance.first_object_token_chars,
		file_type=FileType.UPLOAD,
		owner_pk=instance.owner.pk,
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
	return Group.objects.get(name=settings.SAO_GROUP_NAME)

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
	as_records=False, 
	include_modules = [],
	exclude_modules = ["file_management", "notification_management", "django"],
	filter_query = ''
	):
	values = []
	with open('/tmp/inspectdb', 'w+') as f:
		values = json.loads(management.call_command('show_urls', format="json", stdout=f))
	df = pd.DataFrame(values)
	df["module_app"] = df['module'].str.extract("(\w+)\..*")
	query_list = []
	# # module query
	if len(include_modules) > 0:
		query_list.append(f'module_app.isin({include_modules})')
	query_list.append(f'~module_app.isin({exclude_modules})')
	# # filter query
	if filter_query:
		query_list.append(filter_query)
	df = df.query(" and ".join(query_list))
	logger.info(df.query("url.str.contains('admin')"))
	logger.info(query_list)
	if as_records:
		return df.to_dict(orient='record')
	return df[["url", "module", "name", "module_app"]]

def send_mail(
	subject,
    message,
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=[],
    cc=[],
    bcc=[],
    fail_silently=False,
    auth_user=None,
    auth_password=None,
    connection=None,
    html_message=None,
	allow_sending_on_debug=False
	):
	# restricts sending mail on production
	logger.info(f"""Sending Email settings:
	{settings.DEBUG=}               
	{settings.EMAIL_FORCE_ALLOW=}               
	{settings.EMAIL_BACKEND=}
	{allow_sending_on_debug=}               
	{from_email=}
	{recipient_list=}
	{cc=}
	{bcc=}
	{subject=}
	{message=}
	{html_message=}
	""")
	if any([
			not settings.DEBUG, 
			allow_sending_on_debug, 
			settings.EMAIL_FORCE_ALLOW,
			settings.EMAIL_BACKEND!="django.core.mail.backends.smtp.EmailBackend"
		]):
		connection = connection or get_connection(
			username=auth_user,
			password=auth_password,
			fail_silently=fail_silently,
		)
		message = strip_tags(html_message)

		mail = EmailMultiAlternatives(
			subject, message, from_email, recipient_list, 
			connection=connection, bcc=bcc, cc=cc
		)
		if html_message:
			mail.attach_alternative(html_message, "text/html")
		mail.send()
		logger.info(f"Successfully sent mail")
	else:
		logger.warning(f"Failed to send email with {subject=}")