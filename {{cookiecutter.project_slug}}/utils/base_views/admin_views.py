from django import forms
from django.urls import reverse_lazy
from django.contrib import messages
from utils.detail_wrapper.views import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
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
class AdminListView(BaseListView, LoginRequiredMixin):
	template_name='pages/admin/list.html'

class AdminCreateView(BaseCreateView, LoginRequiredMixin):
	template_name='pages/admin/create.html'

class AdminDetailView(BaseDetailView, LoginRequiredMixin):
	template_name='pages/admin/detail.html'

class AdminUpdateView(BaseUpdateView, LoginRequiredMixin):
	template_name='pages/admin/update.html'

class AdminDeleteView(BaseDeleteView, LoginRequiredMixin):
	template_name='pages/admin/delete.html'

class AdminCreateFormCollectionView(BaseCreateFormCollectionView, LoginRequiredMixin):
	template_name='pages/admin/create.html'

class AdminUpdateFormCollectionView(BaseUpdateFormCollectionView, LoginRequiredMixin):
	template_name='pages/admin/update.html'