from django.shortcuts import render
from base_models.models import Verification
from utils.base_views.ajax.views import (
	BaseListAjaxView,
)

# Create your views here.

class VerificationListAjaxView(BaseListAjaxView):
	model = Verification