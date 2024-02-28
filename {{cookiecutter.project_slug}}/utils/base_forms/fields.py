"""
Custome fields that may need to be overridden due to custom default widgets
WHY DO THIS?
* To reduce requirement for custom forms when defaults are set in models

Reference: https://stackoverflow.com/questions/28497119/change-default-widgets-of-django-to-custom-ones
"""

from formset.widgets import Selectize, SelectizeMultiple, DateInput, UploadedFileInput, DateTimeInput
from formset.richtext.widgets import RichTextarea
from django import forms
import logging
logger = logging.getLogger(__name__)

class DateFormField(forms.DateField):
    widget = DateInput

class DateTimeFormField(forms.DateTimeField):
    widget = DateTimeInput

class RichTextareaFormField(forms.CharField):
    widget = RichTextarea

class FileFormField(forms.FileField):
    widget = UploadedFileInput

class ImageFormField(forms.ImageField):
    widget = UploadedFileInput

class ChoiceFormField(forms.ChoiceField):
    widget = Selectize

class MultipleChoiceFormField(forms.MultipleChoiceField):
    widget = SelectizeMultiple