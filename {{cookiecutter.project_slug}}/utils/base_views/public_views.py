from utils.base_views.views import (
    BaseListView,
    BaseCreateView,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
)

import logging
logger = logging.getLogger(__name__)

# Create your views here.
class PublicListView(BaseListView):
	template_name='pages/public/list.html'

class PublicCreateView(BaseCreateView):
	template_name='pages/public/create.html'

class PublicDetailView(BaseDetailView):
	template_name='pages/public/detail.html'

class PublicUpdateView(BaseUpdateView):
	template_name='pages/public/update.html'

class PublicDeleteView(BaseDeleteView):
    pass
