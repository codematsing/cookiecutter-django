from posts.models import Post, BlogPost, ScholarshipPost
from utils.base_views.ajax.views import (
	BaseListAjaxView,
)
from django.template.loader import render_to_string
import logging
logger = logging.getLogger(__name__)

# Create your views here.
from utils.permissions import IsSAOPermissionMixin

class PostListAjaxView(BaseListAjaxView):
	model = Post
	show_date_filters = True
	column_defs = [
		{'name':'pk', 'visible':False},
		{'name':'title'},
		{'name':'updated_at', 'searchable':False},
		{'name':'updated_by'},
		{'name':'published_date', 'searchable':False},
		{'name':'is_published', 'choices':[['True', 'Published'], ['False', 'Draft']]},
		{'name':'action', 'searchable':False},
	]

	def customize_row(self, row, obj):
		row['is_published'] = render_to_string('posts/published_column.html', {'record':obj})
		row['updated_at'] = render_to_string('detail_wrapper/date.html', {'field':obj.updated_at})
		return super().customize_row(row, obj)

class BlogPostListAjaxView(PostListAjaxView):
	model = BlogPost

	def test_func(self):
		return super().test_func() and self.request.user.is_sao

	def customize_row(self, row, obj):
		row['is_published'] = render_to_string('posts/published_column.html', {'record':obj})
		row['updated_at'] = render_to_string('detail_wrapper/date.html', {'field':obj.updated_at})
		row['action'] = render_to_string('tables/action_column_with_delete.html', {'field':obj.updated_at})
		return super().customize_row(row, obj)

class ScholarshipPostListAjaxView(PostListAjaxView):
	model = ScholarshipPost
