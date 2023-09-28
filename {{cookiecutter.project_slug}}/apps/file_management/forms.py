from formset.renderers.bootstrap import FormRenderer
from django import forms
from formset.widgets import SelectizeMultiple

from file_management.models import DocumentMetadata
from utils.base_forms.forms import BaseModelForm
from utils.base_forms.forms import BaseFormCollection

class DocumentMetadataForm(BaseModelForm):
    default_renderer = FormRenderer(
        form_css_classes='row',
        field_css_classes={
            'name': 'mb-2 col-3', 
            'require_for_tags': 'mb-2 col-3', 
            'description': 'mb-2 col-3', 
            },
    )
    pk = forms.IntegerField(
        required=False, widget=forms.HiddenInput()
        )
    class Meta:
        model = DocumentMetadata
        fields = ["name", "description", "require_for_tags"]
        widgets = {
            'description': forms.Textarea(attrs={'rows':1}),
            'require_for_tags': SelectizeMultiple(),
        }

class DocumentMetadataFormCollection(BaseFormCollection):
    min_siblings = 0
    legend = "Additional Documentary Requirements"
    document_form = DocumentMetadataForm()
    add_label = "Add Documents"