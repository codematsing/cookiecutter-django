from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        # social account already exists, so this is just a login
        if sociallogin.is_existing:
            return

        # some social logins don't have an email address
        if not sociallogin.email_addresses:
            return

        # find the first verified email that we get from this sociallogin
        verified_email = None
        for email in sociallogin.email_addresses:
            if email.verified:
                verified_email = email
                break

        # no verified emails found, nothing more to do
        # edit account_email_verification to "none" if email veficiation not needed
        # checks if_staff=True for verified_email
        if settings.ACCOUNT_EMAIL_VERIFICATION=="mandatory" and not verified_email:
            return

        # check if given email address already exists as a verified email on
        # an existing user's account
        try:
            user = get_user_model().objects.filter(email=email.email).first()
            user.first_name = sociallogin.account.extra_data.get("given_name")
            user.last_name = sociallogin.account.extra_data.get("family_name")
            user.username = sociallogin.account.extra_data.get("email").split('@')[0]
            user.save()
            # if it does, connect this new social login to the existing user
            sociallogin.connect(request, user)
        except Exception as e:
            sociallogin.user.username = email.email.split('@')[0]
        return

    def is_open_for_signup(self, request, sociallogin):
        #https://stackoverflow.com/questions/19113623/django-allauth-only-allow-users-from-a-specific-google-apps-domain
        u = sociallogin.user
        # Optionally, set as staff now as well.
        # This is useful if you are using this for the Django Admin login.
        # Be careful with the staff setting, as some providers don't verify
        # email address, so that could be considered a security flaw.
        #u.is_staff = u.email.split('@')[1] == "customdomain.com"
        if settings.ALLOWED_LOGIN_DOMAINS:
            return u.email.split('@')[1] in settings.ALLOWED_LOGIN_DOMAINS
        else:
            return
