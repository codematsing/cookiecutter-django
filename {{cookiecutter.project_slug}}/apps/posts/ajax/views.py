from posts.models import Post
from utils.base_views.ajax.views import (
	BaseListAjaxView,
)
from django.template.loader import render_to_string
import logging
logger = logging.getLogger(__name__)

# Create your views here.

class PostListAjaxView(BaseListAjaxView):
	model = Post
	show_date_filters = True
	column_defs = [
		{'name':'title'},
		{'name':'updated_at', 'title':'Updated At', 'searchable':False},
		{'name':'is_published', 'choices':[[True, 'Published'], [False, 'Draft']]},
	]
	initial_order=[["updated_at", "desc"]]

	def customize_row(self, row, obj):
		row['is_published'] = obj.is_published_as_badge
		row['updated_at'] = render_to_string('detail_wrapper/date.html', {'field':obj.updated_at})
		return super().customize_row(row, obj)