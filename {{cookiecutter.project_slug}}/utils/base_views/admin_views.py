from django import forms
from django.urls import reverse_lazy
from django.contrib import messages
from utils.detail_wrapper.views import DetailView
from dal import autocomplete
from utils.base_views.views import (
    BaseListView,
    BaseCreateView,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
    BaseCreateFormCollectionView,
    BaseUpdateFormCollectionView,
)

import logging
logger = logging.getLogger(__name__)

# Create your views here.
class AdminListView(BaseListView):
	template_name='pages/admin/list.html'

class AdminCreateView(BaseCreateView):
	template_name='pages/admin/create.html'

class AdminDetailView(BaseDetailView):
	template_name='pages/admin/detail.html'

class AdminUpdateView(BaseUpdateView):
	template_name='pages/admin/update.html'

class AdminDeleteView(BaseDeleteView):
	template_name='pages/admin/delete.html'

class AdminCreateFormCollectionView(BaseCreateFormCollectionView):
	template_name='pages/admin/create.html'

class AdminUpdateFormCollectionView(BaseUpdateFormCollectionView):
	template_name='pages/admin/update.html'