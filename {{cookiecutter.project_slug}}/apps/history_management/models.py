from auditlog.models import LogEntry
from django.template.loader import render_to_string
import logging
logger = logging.getLogger(__name__)

class LogEntryProxy(LogEntry):
    @staticmethod
    def get_additional_data_display(additional_data):
        return render_to_string('history_management/additional_data.html', {'additional_data':additional_data})

    class Meta:
        proxy=True