from utils.lambdas import send_mail
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from logging import getLogger
import smtplib

logger = getLogger(__name__)

class Command(BaseCommand):
    help = "attempts to send email back to host user"

    def add_arguments(self, parser):
        # optional
        parser.add_argument(
            "--emails",
            help="Optionally add recipients of test email",
        )

    def testing_via_django(self, **kwargs):
        try:
            tz = timezone.get_current_timezone()
            logger.info("Attempting to send email via django")
            recipient_list = [settings.EMAIL_HOST_USER]
            recipient_list += kwargs['emails'] if isinstance(kwargs['emails'], list) else [kwargs['emails'],]
            send_mail(
                subject=f"Testing via django sent {timezone.now().astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')}",
                message="lorem ipsum",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
                allow_sending_on_debug=True
                )
        except Exception as e:
            logger.exception(e)

    def handle(self, *args, **kwargs):
        logger.info(f"""Testing Email
            EMAIL_HOST: {settings.EMAIL_HOST}
            EMAIL_PORT: {settings.EMAIL_PORT}
            EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}
            EMAIL_HOST_PASSWORD: {settings.EMAIL_HOST_PASSWORD}
            EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}
        """)
        logger.info(f"Recipients added: {kwargs['emails']}")
        self.testing_via_django(**kwargs)