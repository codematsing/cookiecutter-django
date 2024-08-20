from utils.base_forms.forms import BaseModelForm
from formset.renderers.bootstrap import FormRenderer
from formset.richtext.widgets import RichTextarea
from formset.richtext import controls
from formset.richtext.dialogs import SimpleLinkDialogForm

from django import forms
from formset.widgets import Selectize, DualSelector
from guidelines.models import Guideline
from django.urls import resolve
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

class GuidelineForm(BaseModelForm):
    default_renderer = FormRenderer(
        form_css_classes='row',
		fieldset_css_classes="row",
        field_css_classes={
            '*': 'mb-2 col-12',
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # initializing choices on runtime due to circular import
        from utils.lambdas import get_url_df
        third_party_apps_to_exclude = list(set(settings.THIRD_PARTY_APPS).difference({"notifications",}))
        exclude_modules = ["file_management", "django", "debug_toolbar", "hijack"] + settings.DJANGO_APPS + third_party_apps_to_exclude


        exclude_notifications_except_all = "(~name.str.contains('notifications') or name.str.contains('notifications:all'))"
        exclude_urls_with_params = "~url.str.contains('<|>')"
        exclude_delete_and_ajax_urls = f"~name.str.contains('delete|ajax')"
        filter_query = " and ".join([exclude_notifications_except_all, exclude_urls_with_params, exclude_delete_and_ajax_urls])

        choices = get_url_df(
            exclude_modules=exclude_modules,
            filter_query=filter_query
        )
        self.fields['href'].widget.choices = ((row['name'], f"{row['name']} ({row['url']})") for _, row in choices.iterrows())

    class Meta:
        model = Guideline
        fields = ["href", "content", "status"]
        widgets = {
            'href':Selectize(),
            'content': RichTextarea(control_elements=[
                controls.Heading(),
                controls.Bold(),
                controls.Italic(),
                controls.BulletList(),
                controls.HorizontalRule(),
                controls.Separator(),
                controls.ClearFormat(),
                controls.Undo(),
                controls.Redo(),
                controls.DialogControl(SimpleLinkDialogForm()),
            ])
        }