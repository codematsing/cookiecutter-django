from utils.base_views.ajax.views import BaseListAjaxView, BaseDeleteAjaxView, BaseUpdateAjaxView
from notifications.models import Notification
from django.http.response import JsonResponse
from django.template.loader import render_to_string
import logging
from django.template.loader import render_to_string
logger = logging.getLogger(__name__)

class NotificationsListAjaxView(BaseListAjaxView):
	model = Notification

	column_defs = [
		{'name':'pk', 'visible':False},
		{'name':'timestamp'},
		{'name':'verb', 'title':'Subject'},
		{'name':'unread', 'title':'Status', 'choices':((True, 'Unread'), (False, 'Read')), 'initialSearchValue':True},
		{'name':'action'},
	]

	def test_func(self):
		return self.request.user.is_authenticated

	def get_initial_queryset(self, request):
		return self.request.user.notifications.all()

	def customize_row(self, row, obj):
		row['timestamp'] = f"{obj.timestamp.strftime('%Y-%m-%d %I:%M %p')} ({obj.timesince()})"
		row['unread'] = render_to_string("notifications/status_badge.html", context={'record':obj})
		row['action'] = render_to_string("notifications/action.html", context={'record':obj})

class NotificationUpdateUnreadAjaxView(BaseUpdateAjaxView):
	model = Notification

	def get(self, request):
		pk = request.GET.get('notif', None)
		unread = request.GET.get('unread', None)
		qs = self.request.user.notifications.filter(pk=int(pk))
		logger.info(qs)
		logger.info(unread)
		if not qs.exists():
			return JsonResponse(status=403, data={})
		
		if unread=='true':
			qs.mark_all_as_unread()
			logger.info("here")
		else:
			qs.mark_all_as_read()
			logger.info("there")
		obj = qs.first()
		html = '<label class="badge badge-success">Read</label>'
		if obj.unread:
			html = '<label class="badge badge-danger">Unread</label>'
		return JsonResponse({'unread':obj.unread, 'html':html})