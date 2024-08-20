from formset.renderers.bootstrap import FormRenderer
from django import forms
from formset.widgets import SelectizeMultiple, Selectize
from utils.base_forms.forms import PdfFileWidget
from file_management.models import DocumentMetadata, DocumentSubmission
from utils.base_forms.forms import BaseModelForm
from utils.base_forms.forms import BaseFormCollection
from formset.widgets import Selectize
import logging
logger = logging.getLogger(__name__)

class DocumentMetadataForm(BaseModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
		fieldset_css_classes="row",
        field_css_classes={
            "name": "mb-2 col-6",
            "description": "mb-2 col-6",
        },
    )
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = DocumentMetadata
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 1}),
            "require_for_tags": SelectizeMultiple(),
        }


class DocumentMetadataFormset(BaseFormCollection):
    min_siblings = 0
    document_form = DocumentMetadataForm()
    legend = "Additional Documentary Requirements"
    add_label = "Add Documents"


class DocumentSubmissionForm(BaseModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
		fieldset_css_classes="row",
        field_css_classes={
            "metadata": "col-md-12 align-self-center",
            # 'description': 'col-md-6 align-self-center',
            "attachment": "col-md-6",
        },
    )
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    attachment = forms.FileField(
        required=False, widget=PdfFileWidget(),
        help_text='Accepts only PDF. Maximum of 10MB'
    )
    field_order = ["id", "metadata", "attachment"]

    class Meta:
        model = DocumentSubmission
        fields = ["metadata", "attachment"]
        widgets = {
            "metadata": Selectize,
        }
        disabled_fields = [
            "metadata",
        ]


class DocumentSubmissionWMetadataSelectionForm(BaseModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
		fieldset_css_classes="row",
        field_css_classes={
            "metadata": "col-md-12 align-self-center",
            # 'description': 'col-md-6 align-self-center',
            "attachment": "col-md-6",
            "notes": "col-md-6",
        },
    )
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    attachment = forms.FileField(
        required=False, widget=PdfFileWidget(),
        help_text='Accepts only PDF. Maximum of 10MB'
    )
    field_order = ["id", "metadata", "attachment"]

    class Meta:
        model = DocumentSubmission
        fields = ["metadata", "attachment", "notes"]
        widgets = {
            "metadata": Selectize,
        }


class DocumentSubmissionFormset(BaseFormCollection):
    min_siblings = 1
    legend = "Documents"
    document_form = DocumentSubmissionWMetadataSelectionForm()
    add_label = "Add Document"

    def save(self):
        for document_form in self.cleaned_data:
            document_kwargs = document_form['document_form']
            document = DocumentSubmission.objects.create(owner=self.request.user, **document_kwargs)
            logger.info(document)
        return self.request.user
