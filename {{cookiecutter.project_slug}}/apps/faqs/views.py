from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import FaqItem
from utils.base_views.views import (
	
	BaseDeleteView,
	BaseActionView,
	BaseAddObjectView,
	BaseRemoveObjectView,
	BaseActionObjectView,
)
from django.urls import reverse_lazy
from faqs.forms import FaqCollectionForm, FaqItemForm

from utils.base_views.public_views import PublicListView

from utils.base_views.admin_views import (
	AdminListView,
	AdminCreateView,
	AdminDetailView,
	AdminUpdateView,
	AdminDeleteView,
)


import logging
logger = logging.getLogger(__name__)

# Create your views here.
class FaqListView(PublicListView):
	model = FaqItem
	template_name = "faqs/list.html"

	def get_queryset(self):
		logger.info(super().get_queryset().filter(is_published=True))
		return super().get_queryset().filter(is_published=True)

class ManagedFaqListView(AdminListView):
	model = FaqItem

class ManagedFaqItemCreateView(AdminCreateView):
	model = FaqItem
	form_class = FaqItemForm

class ManagedFaqItemDetailView(AdminDetailView):
	model = FaqItem

class ManagedFaqItemUpdateView(AdminUpdateView):
	model = FaqItem
	form_class = FaqItemForm

class ManagedFaqItemDeleteView(AdminDeleteView):
	model = FaqItem


# class ManagedFaqListFormView(AdminFormCollectionView):
# 	model = FaqItem
# 	collection_class = FaqCollectionForm
# 	form_header = "FAQ Items"

# 	def get_initial(self):
# 		return [
# 			{
# 				'faq_item_form': {
# 					field.name: getattr(faq, field.name)
# 					for field in faq._meta.fields
# 				}
# 			} for faq in self.model.objects.all()
# 		]

# 	def get_success_url(self):
# 		return reverse_lazy("faqs_management:list")

# 	def get_success_message(self, cleaned_data):
# 		return "FAQs saved"