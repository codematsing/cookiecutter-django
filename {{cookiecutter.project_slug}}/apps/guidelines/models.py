from django.db import models
from utils.base_models.models import AbstractAuditedModel, BaseModelManager

# Create your models here.
class GuidelineManager(BaseModelManager):
    pass

class GuidelineStatus(models.TextChoices):
    DRAFT = "DRAFT", "DRAFT"
    COMPLETE = "COMPLETE", "COMPLETE"

class Guideline(AbstractAuditedModel):
    objects = GuidelineManager()

    href = models.CharField(max_length=64, null=False, blank=False, verbose_name="Where will the guideline be shown?")
    content = models.TextField()
    status = models.CharField(choices=GuidelineStatus.choices, default=GuidelineStatus.DRAFT)

    def __str__(self):
        return self.href

    class Meta:
        # https://docs.djangoproject.com/en/4.2/ref/models/options/
        db_table_comment = "Brief description about guidelines"
        verbose_name = "Guideline"
        verbose_name_plural = "Guidelines"
        app_label = "guidelines"
        default_related_name = "guidelines"
        # ordering = []
        # get_latest_by = []
        # unique_together = []
    #     permissions = [
    #         ('add_guideline_<model_fk>', 'Can add Guideline <model_fk>'),
    #         ('change_guideline_<model_fk>', 'Can change Guideline <model_fk>'),
    #         ('view_guideline_<model_fk>', 'Can view Guideline <model_fk>'),
    #         ('remove_guideline_<model_fk>', 'Can remove Guideline <model_fk>'),
    #         ('delete_guideline_<model_fk>', 'Can delete Guideline <model_fk>'),
    #     ]

    # ensure to override if needed. See AbstractBaseModel for default url methods:
    # * get_list_url
    # * get_create_url
    # * get_absolute_url
    # * get_update_url
    # * get_delete_url
    # * add additional urls related to model if needed. see urls.py