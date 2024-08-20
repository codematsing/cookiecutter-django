from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)


class UnitRoleConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'unit_roles'

	def ready(self):
		try: 
			import unit_roles.signals
			logger.info("Imported unit_roles.signals")
		except ImportError as e:
			logging.exception(e)
			logger.warning("Unsuccessful signal import unit_roles")
