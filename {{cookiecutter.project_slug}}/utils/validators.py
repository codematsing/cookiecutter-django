from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.conf import settings

class EmailValidator(EmailValidator):
    allowlist = settings.ALLOWED_LOGIN_DOMAINS