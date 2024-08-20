from django.db.models.signals import post_save, m2m_changed, pre_delete
from django.dispatch import receiver
from file_management.models import DocumentSubmission
from django.contrib.auth import get_user_model
from django.conf import settings
from notifications.signals import notify
from django.urls import reverse
import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=DocumentSubmission)
def notify_saos_of_file_upload(sender, instance, created, **kwargs):
    logger.info(f"{type(instance)} POST SAVE")
    logger.info(f"params:\nsender={sender}\ninstance={instance}\ncreated={created}\nkwargs={kwargs}")
    _object = instance.content_object
    message = f"{instance.updated_by} uploaded file ({instance.metadata}) to {_object}"
    if hasattr(_object, 'get_absolute_url'):
        notify.send(
            instance,
            recipient=get_user_model().objects.filter(groups__name=settings.SAO_GROUP_NAME),
            verb=message,
            url=_object.get_absolute_url()
        )

# @receiver(pre_delete, sender=FileManagement)
# def file_managemen_post_save(sender, instance, **kwargs):
#     logger.info(f"{type(instance)} PRE SAVE")
#     logger.info(f"params:\nsender={sender}\ninstance={instance}\nkwargs={kwargs}")
#     if instance.pk == None: #for creation
#         pass
#     else:
#         pass

# @receiver(m2m_changed, sender=FileManagement.<model_fk>.through)
# def file_managemen_<model_fk>_changed(sender, instance, action, reverse, model, pk_set, using):
#     logger.info(f"{type(instance)} Document M2M CHANGED")
#     logger.info(f"params:\nsender={sender}\ninstance={instance}\naction={action}\nreverse={reverse}\nmodel={model}\npk_set={pk_set}\nkwargs={kwargs}")
#     if action=='post_add':
#         pass
#     elif action=='post_remove':
#         pass