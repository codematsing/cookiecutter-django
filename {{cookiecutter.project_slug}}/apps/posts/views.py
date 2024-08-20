from typing import Any, List, Sequence
from django.core.files.base import File

from django.db.models.query import QuerySet
from utils.base_views.public_views import (
    PublicListView,
    PublicDetailView,
)

from utils.base_views.admin_views import (
    AdminListView,
    AdminCreateView,
    AdminUpdateView,
    AdminDeleteView,
    AdminCreateFormCollectionView
)
from django.utils import timezone

from posts.forms import PostForm
from posts.models import Post
from django.urls import reverse_lazy

import logging
logger = logging.getLogger(__name__)

# Create your views here.
class PostListView(PublicListView):
    model = Post
    paginate_by = 8
    template_name = 'posts/list.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs.filter(is_published=True)

class ManagedPostListView(AdminListView):
    model = Post

class ManagedPostCreateView(AdminCreateView):
    model = Post
    form_class = PostForm

class PostDetailView(PublicDetailView):
    model = Post
    template_name = 'posts/detail.html'

class ManagedPostUpdateView(AdminUpdateView):
    model = Post
    form_class = PostForm

class ManagedPostDeleteView(AdminDeleteView):
    model = Post
