from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)


class NotificationManagementConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'notification_management'

	def ready(self):
		try: 
			import notification_management.signals
			logger.info("Imported notification_management.signals")
		except ImportError as e:
			logging.exception(e)
			logger.warning("Unsuccessful signal import notification_management")
