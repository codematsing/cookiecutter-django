from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)


class ModuleManagementConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'module_management'

	def ready(self):
		try: 
			import module_management.signals
			logger.info("Imported module_management.signals")
		except ImportError as e:
			logging.exception(e)
			logger.warning("Unsuccessful signal import module_management")
