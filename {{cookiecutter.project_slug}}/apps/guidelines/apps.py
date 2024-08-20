from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)


class GuidelineConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'guidelines'

	def ready(self):
		try: 
			import guidelines.signals
			logger.info("Imported guidelines.signals")
		except ImportError as e:
			logging.exception(e)
			logger.warning("Unsuccessful signal import guidelines")
