from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MaxValueValidator
from utils.base_models.models import AbstractAuditedModel

import datetime
import os


# Create your models here.

class Registration(AbstractAuditedModel):
    first_name = models.CharField(
        max_length = 128
    )

    last_name = models.CharField(
        max_length = 128
    )

    birth_date = models.DateField(
        blank=False,
        null=False,
        validators=[
            MaxValueValidator(limit_value=datetime.date.today)
        ]
    )

    student_number = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(
                code="Invalid Student Number",
                message="Must be numeric. Must not contain symbols or letters",
                regex="^\\d+$",
            )
        ],
        unique=True,
    )

    email = models.EmailField(
        max_length=128,
        unique=True,
        verbose_name="Alternative Email",
        help_text="Please provide email to notify you once user registration has been approved"
    )

    is_approved = models.BooleanField(null=True, blank=True, verbose_name="Approval Status", choices=((True, "Approved"), (False, "Rejected")))

    def __str__(self):
        return self.email

    def as_card(self, **kwargs):
        return super().as_card(exclude=["is_approved"])

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
