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
    BaseFormCollectionView
)

import logging
logger = logging.getLogger(__name__)

# Create your views here.
class AdminListView(LoginRequiredMixin, BaseListView):
	template_name='pages/admin/list.html'

class AdminCreateView(LoginRequiredMixin, BaseCreateView):
	template_name='pages/admin/create.html'

class AdminDetailView(LoginRequiredMixin, BaseDetailView):
	template_name='pages/admin/detail.html'

class AdminUpdateView(LoginRequiredMixin, BaseUpdateView):
	template_name='pages/admin/update.html'

class AdminDeleteView(LoginRequiredMixin, BaseDeleteView):
	template_name='pages/admin/delete.html'

class AdminFormCollectionView(LoginRequiredMixin, BaseFormCollectionView):
	template_name='pages/admin/form.html'

class AdminCreateFormCollectionView(LoginRequiredMixin, BaseCreateFormCollectionView):
	template_name='pages/admin/create.html'

class AdminUpdateFormCollectionView(LoginRequiredMixin, BaseUpdateFormCollectionView):
	template_name='pages/admin/update.html'