from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)


class FaqConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'faqs'

	def ready(self):
		try: 
			import faqs.signals
			logger.info("Imported faqs.signals")
		except ImportError as e:
			logging.exception(e)
			logger.warning("Unsuccessful signal import faqs")
