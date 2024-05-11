from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)


class GroupManagementConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'group_management'

	def ready(self):
		try: 
			import group_management.signals
			logger.info("Imported group_management.signals")
		except ImportError as e:
			logging.exception(e)
			logger.warning("Unsuccessful signal import group_management")
