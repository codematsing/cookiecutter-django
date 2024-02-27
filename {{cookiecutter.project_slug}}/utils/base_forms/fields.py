"""
Custome fields that may need to be overridden due to custom default widgets
WHY DO THIS?
* To reduce requirement for custom forms when defaults are set in models

Reference: https://stackoverflow.com/questions/28497119/change-default-widgets-of-django-to-custom-ones
"""

from formset.widgets import Selectize, SelectizeMultiple, DateInput, UploadedFileInput
from formset.richtext.widgets import RichTextarea
from django import forms

class DateFormField(forms.DateField):
    widget = DateInput

class RichTextareaFormField(forms.Textarea):
    widget = RichTextarea

class FileFormField(forms.FileField):
    widget = UploadedFileInput

class ImageFormField(forms.ImageField):
    widget = UploadedFileInput

class ModelChoiceFormField(forms.ModelChoiceField):
    widget = Selectize

class ModelMultipleChoiceFormField(forms.ModelMultipleChoiceField):
    widget = SelectizeMultiple


