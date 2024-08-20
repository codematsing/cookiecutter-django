from django.shortcuts import render
from faqs.models import FaqItem
from utils.base_views.ajax.views import (
	BaseListAjaxView,
)
from django.template.loader import render_to_string

# Create your views here.

class FaqItemListAjaxView(BaseListAjaxView):
	model = FaqItem

	column_defs = [
		{'name':'pk', 'visible':False},
		{'name':'question'},
		{'name':'answer'},
		{'name':'is_published'},
		{'name':'action'},
	]

	def customize_row(self, row, obj):
		row['answer'] = obj.answer # renders html template
		row['is_published'] = render_to_string('faqs/published_column.html', {'record':obj})
		row['action'] = render_to_string('tables/action_column.html', {'record':obj, 'has_update_permission':True})