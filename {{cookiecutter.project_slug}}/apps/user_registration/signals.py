import random
import string
import logging
import base64

from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from utils.lambdas import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth import get_user_model
from utils.lambdas import get_current_domain

from user_registration.models import Registration
from notifications.signals import notify

logger = logging.getLogger(__name__)

@receiver(post_delete, sender=Registration)
def user_registration_post_delete(sender, instance, **kwargs):
    logger.info(f"{type(instance)} POST DELETE")
    logger.info(f"params:\nsender={sender}\ninstance={instance}\nkwargs={kwargs}")
    try:
        send_mail(
            "[SIKAP] User Registration Rejected",
            "User rejected",
            settings.EMAIL_HOST_USER,
            [instance.email],
            html_message=render_to_string('email/user_rejected.html', {'object': instance}),
            allow_sending_on_debug=True
        )
    except Exception as e:
        pass


@receiver(post_save, sender=Registration)
def user_registration_post_update(sender, instance, created, **kwargs):
    if created:
        notify.send(
            instance,
            recipient=get_user_model().objects.filter(groups__name=settings.SAO_GROUP_NAME),
            verb="You have one new account registration request from {}".format(instance),
            url=reverse("user_registration:list")
        )

    if instance.is_approved:
        decrypted_code = "{}_{}_{}".format(instance.id, instance.student_number, instance.email)
        encrypted_code = base64.b64encode(decrypted_code.encode("utf-8")).decode('utf-8')
        signup_page = reverse("approved_signup", kwargs={"signup_code":encrypted_code})
        signup_url = f"{get_current_domain()}{signup_page}"
        try:
            send_mail(
                "[SIKAP] User Registration Approved",
                f"User approved, you may now signup with this link: {signup_url}",
                settings.EMAIL_HOST_USER,
                [instance.email],
                html_message=render_to_string('email/user_approved.html', {
                    'object': instance,
                    'signup_url': signup_url,
                }),
                allow_sending_on_debug=True
            )
        except Exception as e:
            pass