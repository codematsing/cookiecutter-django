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
	def is_qao(self):
		return self.is_superuser or self.is_staff or self.groups.filter(name=settings.QAO_GROUP_NAME).exists()

	@property
	def primary_unit(self):
		primary_unit_role = self.unit_roles.objects.filter(is_primary_unit_role=True)
		if primary_unit_role.exists():
			return primary_unit_role.first()
		return None

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

	@property
	def projects(self):
		from members.models import Member
		from projects.models import Project

		projects = Member.objects.filter(email=self.email).values_list("project", flat=True).distinct()
		return Project.objects.filter(id__in=projects)

	@property
	def for_approval_projects(self):
		from members.models import Member
		from projects.models import Project
		projects = Project.objects.filter(approval_events__state__authorized_roles__in=self.unit_roles.all().values_list['roles'])
		return Project.objects.filter(id__in=projects)

	@property
	def editable_projects(self):
		from members.models import Member
		from members.models import AccessType
		from projects.models import Project

		projects = Member.objects.filter(
			email=self.email, access_type=AccessType.EDITOR
		).values_list("project", flat=True).distinct()
		return Project.objects.filter(id__in=projects)

	def can_view_project(self, project):
		# can view if qao or if member of project
		approvers_authorized_role_ids = project.approval_events.values_list('state__authorized_roles', flat=True)
		return self.is_qao or self.projects.filter(id=project.id).exists() or self.groups.filter(
			# unit=project.proponent_unit,
			pk__in=approvers_authorized_role_ids,
		).exists()

	def is_project_approver(self, project):
		approvers_authorized_role_ids = project.approval_events.filter().first().state.authorized_roles.values_list('pk', flat=True)
		return self.groups.filter(
			# unit=project.proponent_unit,
			# role__pk__in=approvers_authorized_role_ids
			pk__in=approvers_authorized_role_ids,
		).exists()

	def can_approve_project(self, project):
		approval_event = (project.approval_events.filter(approver_action__isnull=True) | project.approval_events.filter(approver_action__in=[-1,0])).first()
		approvers_authorized_role_ids = approval_event.state.authorized_roles.values_list('pk', flat=True)
		return self.groups.filter(
			# unit=project.proponent_unit,
			# role__pk__in=approvers_authorized_role_ids
			pk__in=approvers_authorized_role_ids,
		).exists()

	def can_edit_project(self, project):
		return self.is_superuser or self.editable_projects.filter(id=project.id).exists()

	def get_absolute_url(self):
		"""Get url for user's detail view.

		Returns:
			str: URL for user detail.

		"""
		return reverse("home")
		return reverse("users:detail", kwargs={"username": self.username})

	def get_profile_update_url(self):
		return reverse("profile:update")

	@property
	def get_profile_required_fields(self):
		return [
			'honorifics',
			'first_name',
			'last_name',
			'employee_number',
		]