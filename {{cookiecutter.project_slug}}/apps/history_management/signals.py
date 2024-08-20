from auditlog.signals import post_log, prelog
from auditlog.receivers import log_create
from django.dispatch import receiver
from auditlog.models import LogEntry
from django.db.models.signals import post_save, m2m_changed, pre_delete
from django.contrib.contenttypes.models import ContentType
import logging
logger = logging.getLogger(__name__)

# @receiver(post_save)
# def force_logentry_for_additional_data():
#     LogEntry.objects.create(
#                 actor_id=request.user.id,
#                 content_type_id=ContentType.objects.get_for_model(my_object).pk,
#                 object_id=object_id,
#                 object_pk=object_id,
#                 object_repr=str(my_object),
#                 action=1,  # 0 for create, 1 for update, 2 for delete
#                 changes=json.dumps({
#                     "field_name1": ["from_value", "to_value"],
#                     "field_name2": ["from_value", "to_value"]
#                 }),