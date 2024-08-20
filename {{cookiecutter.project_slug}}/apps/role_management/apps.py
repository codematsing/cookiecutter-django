from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)


class RoleManagementConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'role_management'

	def ready(self):
		try: 
			import role_management.signals
			logger.info("Imported role_management.signals")
		except ImportError as e:
			logging.exception(e)
			logger.warning("Unsuccessful signal import role_management")
