"""
Custome fields that may need to be overridden due to custom default widgets
WHY DO THIS?
* To reduce requirement for custom forms when defaults are set in models

Reference: https://stackoverflow.com/questions/28497119/change-default-widgets-of-django-to-custom-ones
"""
from django.db import models
from formset.widgets import Selectize, DatePicker, UploadedFileInput
from formset.richtext.widgets import RichTextarea
from django import forms

# custom date field
class DateFormField(forms.DateField):
    widget = DatePicker

class DatePickerField(DateFormField):
    def formfield(self, **kwargs):
        defaults = {'form_class': DateFormField}
        defaults.update(kwargs)
        return super(models.DateField, self).formfield(**defaults)

# custom richtextarea
class RichTextareaFormField(forms.Textarea):
    widget = RichTextarea

class RichTextareaField(RichTextareaFormField):
    def formfield(self, **kwargs):
        defaults = {'form_class': RichTextareaFormField}
        defaults.update(kwargs)
        return super(models.TextField, self).formfield(**defaults)

# custom file field
class FileFormField(forms.FileField):
    widget = UploadedFileInput

class FileField(FileFormField):
    def formfield(self, **kwargs):
        defaults = {'form_class': FileFormField}
        defaults.update(kwargs)
        return super(models.FileField, self).formfield(**defaults)

# custom file field
class ImageFormField(forms.ImageField):
    widget = UploadedFileInput

class ImageField(ImageFormField):
    def formfield(self, **kwargs):
        defaults = {'form_class': ImageFormField}
        defaults.update(kwargs)
        return super(models.ImageField, self).formfield(**defaults)
    
# in models.py
# import utils.base_models import fields
# class Model(models.Model)
#     date = fields.DatePickerField()
#     content = fields.RichTextareaField()
#     attachment = fields.FileField()
#     image = fields.ImageField()