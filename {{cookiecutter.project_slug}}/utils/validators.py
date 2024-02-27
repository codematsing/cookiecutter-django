from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.utils.regex_helper import _lazy_re_compile
from utils.lambdas import current_year
import re
import logging
logger = logging.getLogger(__name__)

class EmailValidator(EmailValidator):
    allowlist = settings.ALLOWED_LOGIN_DOMAINS

class UPEmailValidator(EmailValidator):
    domain_regex = _lazy_re_compile(r'up.*\.edu.ph', re.IGNORECASE)
    message = "Must be valid UP email"

def validate_academic_year_range(value):
    split_values = value.split('-')
    if len(split_values)==2 and all(val.isnumeric() for val in split_values):
        start = int(split_values[0])
        end = int(split_values[1])
        next_year = current_year()+1
        if end <= next_year and end-start==1:
            return None
        else:
            raise ValidationError(f"End year must not surpass year {next_year}")
    raise ValidationError("Requires that format is YYYY-YYYY+1")

def get_errors(instance: models):
    """Supplemental checking for forms

    Args:
        instance (models): any model instance

    # Returns:
        dict: field errors
    """
    try:
        instance.full_clean()
        return {}
    except Exception as e:
        logger.warning(vars(instance))
        logger.warning(e)
        return dict(e)