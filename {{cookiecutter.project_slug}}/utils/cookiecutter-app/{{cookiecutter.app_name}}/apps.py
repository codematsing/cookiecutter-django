from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)


class {{cookiecutter.camel_case_app_name}}Config(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = '{{cookiecutter.app_location}}'

	def ready(self):
		try: 
			import {{cookiecutter.app_location}}.signals
			logger.info("Imported {{cookiecutter.app_location}}.signals")
		except ImportError as e:
			logging.exception(e)
			logger.warning("Unsuccessful signal import {{cookiecutter.app_location}}")
