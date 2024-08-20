from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import CharField, TextChoices
from utils.base_models.models import AbstractAuditedModel, BaseModelManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class HonorificTitles(TextChoices):
	MX = "Mx.", "Mx."
	MR = "Mr.", "Mr."
	MS = "Ms.", "Ms."
	MRS = "Mrs.", "Mrs."
	PROF = "Prof.", "Prof."
	DR = "Dr.", "Dr."

class UserManager(BaseModelManager, UserManager):
	pass

class User(AbstractUser, AbstractAuditedModel):
	objects = UserManager()
	"""
	Default custom user model for UPD Quality Assurance Office Academic Program Improvement System.
	If adding fields that need to be filled at user signup,
	check forms.SignupForm and forms.SocialSignupForms accordingly.
	"""

	#: First and last name fields already exists in AbstractUser model
	first_name = CharField(_("First Name"), max_length=150, null=True, blank=True)
	last_name = CharField(_("Last Name"), max_length=150, null=True, blank=True)
	middle_name = CharField(_("Middle Name"), max_length=150, null=True, blank=True)
	suffix = CharField(_("Suffix"), max_length=150, null=True, blank=True)
	honorifics = CharField(_("Honorifics"), max_length=5, null=True, blank=True, choices=HonorificTitles.choices, default=HonorificTitles.MX)
	employee_number = CharField(_("Employee No."), max_length=64, null=True, blank=True)

	def as_card(self):
		return super().as_card(fields=[
			'honorifics',
			'first_name',
			'middle_name',
			'last_name',
			'suffix',
			'username', 
			'email_address',
			'employee_number',
			'last_login'
			])

	@property
	def salutation(self):
		name_parts = [
			self.honorifics,
			self.first_name,
			self.middle_name,
			self.last_name,
			self.suffix,
		]
		return " ".join([part for part in name_parts if part])

	@property
	def full_name(self):
		name_parts = [
			self.first_name,
			self.middle_name,
			self.last_name,
			self.suffix,
		]
		return " ".join([part for part in name_parts if part])

	@property
	def short_name(self):
		name_parts = [
			self.first_name,
			self.last_name,
		]
		return " ".join([part for part in name_parts if part])

	def __str__(self):
		if self.short_name:
			return f"{self.short_name} ({self.username})"
		else:
			return f"{self.username}"

	def get_absolute_url(self):
		"""Get url for user's detail view.

		Returns:
			str: URL for user detail.

		"""
		return reverse("home")
		return reverse("users:detail", kwargs={"username": self.username})

	def get_profile_update_url(self):
		return reverse("profile:update")