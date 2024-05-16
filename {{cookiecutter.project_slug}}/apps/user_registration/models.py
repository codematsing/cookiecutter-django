from django.db import models
from django.urls import reverse
from utils import lambdas
from utils.base_models import fields

# Create your models here.
class Registration(models.Model):
    first_name = models.CharField(
        max_length = 128
    )

    last_name = models.CharField(
        max_length = 128
    )

    email = models.EmailField(
        max_length=128,
        unique=True,
    )

    message = models.EmailField(
        verbose_name="Message to moderator for user registration",
        max_length=1024,
    )

    is_approved = models.BooleanField(default=None, null=True, blank=True, choices=((None, "Unknown"), (True, "Approved"), (False, "Declined")))
    created_at = fields.DateTimeField(auto_now_add=True)
    attachment = fields.FileField(upload_to=lambdas.internal_upload)


    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse(
            "user_registration:detail",
            kwargs={"pk": self.pk}
            )

    def get_update_url(self):
        return reverse(
            "user_registration:update",
            kwargs={"pk": self.pk}
            )

    def get_delete_url(self):
        return reverse(
            "user_registration:delete",
            kwargs={"pk": self.pk}
            )

    def get_approve_url(self):
        return reverse(
            "user_registration:approve",
            kwargs={"pk": self.pk}
            )

    def get_reject_url(self):
        return reverse(
            "user_registration:reject",
            kwargs={"pk": self.pk}
            )
