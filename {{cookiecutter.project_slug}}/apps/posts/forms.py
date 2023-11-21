from django import forms
from formset.widgets import SelectizeMultiple, UploadedFileInput
from formset.richtext.widgets import RichTextarea
from utils.base_forms.forms import BaseModelForm
from .models import Post

class PostForm(BaseModelForm):
    body = forms.CharField(widget=RichTextarea(), required=False)

    class Meta:
        model = Post
        exclude = ['history_remarks']
        widgets = {
            'thumbnail': UploadedFileInput(),
        }
