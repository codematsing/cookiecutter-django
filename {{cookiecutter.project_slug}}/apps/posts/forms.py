from django import forms
from utils.base_forms.forms import ImageFileWidget
from formset.richtext.widgets import RichTextarea
from utils.base_forms.forms import BaseModelForm
from .models import Post

class PostForm(BaseModelForm):
    body = forms.CharField(widget=RichTextarea(), required=False)

    class Meta:
        model = Post
        widgets = {
			'thumbnail': ImageFileWidget(),
			'is_published': forms.RadioSelect(),
        }
        fields = '__all__'
