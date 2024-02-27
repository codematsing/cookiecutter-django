from posts.models import Post
from utils.base_views.ajax.views import (
	BaseListAjaxView,
	BaseCreateAjaxView,
	BaseDetailAjaxView,
	BaseUpdateAjaxView,
	BaseDeleteAjaxView,
)
from django.template.loader import render_to_string
import logging
logger = logging.getLogger(__name__)

# Create your views here.

class PostListAjaxView(BaseListAjaxView):
	model = Post
	show_date_filters = True
	column_defs = [
		{'name':'pk', 'visible':False},
		{'name':'title'},
		{'name':'updated_at', 'title':'Updated At', 'searchable':False},
		{'name':'is_published', 'choices':[[True, 'Published'], [False, 'Draft']]},
		{'name':'action', 'searchable':False},
	]

	def customize_row(self, row, obj):
		row['is_published'] = obj.is_published_as_badge
		row['updated_at'] = render_to_string('detail_wrapper/date.html', {'field':obj.updated_at})
		return super().customize_row(row, obj)

class PostCreateAjaxView(BaseCreateAjaxView):
	model = Post

class PostDetailAjaxView(BaseDetailAjaxView):
	model = Post

class PostUpdateAjaxView(BaseUpdateAjaxView):
	model = Post

class PostDeleteAjaxView(BaseDeleteAjaxView):
	model = Post