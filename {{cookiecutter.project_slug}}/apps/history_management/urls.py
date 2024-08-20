from django.urls import path, include
from .views import (
    HistoryListAjaxView,
)
app_name = "history"

# Make sure you add urls to model.spy
# add get_<name>_url() method

urlpatterns = [
    # list
    path(
        "",
        HistoryListAjaxView.as_view(),
        name="list"
    ),
]