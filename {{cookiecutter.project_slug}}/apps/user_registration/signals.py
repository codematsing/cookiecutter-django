import random
import string
import logging

from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from utils.lambdas import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse

from user_registration.models import Registration

logger = logging.getLogger(__name__)



@receiver(post_delete, sender=Registration)
def user_registration_post_delete(sender, instance, **kwargs):
    logger.info(f"{type(instance)} POST DELETE")
    logger.info(f"params:\nsender={sender}\ninstance={instance}\nkwargs={kwargs}")
    try:
        send_mail(
            "[{{cookiecutter.project_name}}] User Registration Rejected",
            "User rejected",
            settings.EMAIL_HOST_USER,
            [instance.email],
            html_message=render_to_string('email/user_rejected.html', {'object': instance}),
            allow_sending_on_debug=True,
        )
    except Exception as e:
        pass


@receiver(post_save, sender=Registration)
def user_registration_post_update(sender, instance, **kwargs):
    if instance.is_approved:
        try:
            send_mail(
                "[{{cookiecutter.project_name}}] User Registration Approved",
                "User approved, you may now signup with this link: ",
                settings.EMAIL_HOST_USER,
                [instance.email],
                html_message=render_to_string('email/user_approved.html', {
                    'object': instance
                }),
                allow_sending_on_debug=True
            )
        except Exception as e:
            pass
