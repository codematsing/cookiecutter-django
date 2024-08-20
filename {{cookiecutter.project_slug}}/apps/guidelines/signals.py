from django.db.models.signals import post_save, m2m_changed, pre_delete
from django.dispatch import receiver
from guidelines.models import Guideline
import logging
logger = logging.getLogger(__name__)

# @receiver(post_save, sender=Guideline)
# def guideline_post_save(sender, instance, created, **kwargs):
#     logger.info(f"{type(instance)} POST SAVE")
#     logger.info(f"params:\nsender={sender}\ninstance={instance}\ncreated={created}\nkwargs={kwargs}")
#     if created:
#         pass
#     else:
#         pass

# @receiver(pre_delete, sender=Guideline)
# def guideline_post_save(sender, instance, **kwargs):
#     logger.info(f"{type(instance)} PRE SAVE")
#     logger.info(f"params:\nsender={sender}\ninstance={instance}\nkwargs={kwargs}")
#     if instance.pk == None: #for creation
#         pass
#     else:
#         pass

# @receiver(m2m_changed, sender=Guideline.<model_fk>.through)
# def guideline_<model_fk>_changed(sender, instance, action, reverse, model, pk_set, using):
#     logger.info(f"{type(instance)} Document M2M CHANGED")
#     logger.info(f"params:\nsender={sender}\ninstance={instance}\naction={action}\nreverse={reverse}\nmodel={model}\npk_set={pk_set}\nkwargs={kwargs}")
#     if action=='post_add':
#         pass
#     elif action=='post_remove':
#         pass