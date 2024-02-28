from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)


class {{cookiecutter.app_name_snake_case_plural_camel_case}}Config(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = '{{cookiecutter.app_location_dot_notation}}'

	def ready(self):
		try: 
			import {{cookiecutter.app_location_dot_notation}}.signals
			logger.info("Imported {{cookiecutter.app_location_dot_notation}}.signals")
		except ImportError as e:
			logging.exception(e)
			logger.warning("Unsuccessful signal import {{cookiecutter.app_location_dot_notation}}")
