from factory import (
    lazy_attribute
)
from portfolios.models import AbstractAuditedProfile
from factory.django import DjangoModelFactory
from auxiliaries.status_tags.form_status.models import FormStatus

class AbstractAuditedProfileFactory(DjangoModelFactory):
    @lazy_attribute
    def status(self):
        return FormStatus.objects.update_or_create(name="Submitted")[0]

    class Meta:
        model = AbstractAuditedProfile