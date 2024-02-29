"""
Custome fields that may need to be overridden due to custom default widgets
WHY DO THIS?
* To reduce requirement for custom forms when defaults are set in models

Reference: https://stackoverflow.com/questions/28497119/change-default-widgets-of-django-to-custom-ones
"""
from django.db import models
from django import forms
from django.utils import timezone
import uuid
import os
import logging
logger = logging.getLogger(__name__)

from formset.widgets import Selectize, SelectizeMultiple, DateInput, UploadedFileInput, DateTimeInput, DualSelector
from formset.richtext.widgets import RichTextarea

# custom fields that presets to datefield widget
class DateField(models.DateField):
    def formfield(self, **kwargs):
        form_class = super().formfield(**kwargs)
        form_class.widget = DateInput()
        return form_class

# custom fields that presets to datetimefield widget
class DateTimeField(models.DateTimeField):
    def formfield(self, **kwargs):
        form_class = super().formfield(**kwargs)
        form_class.widget = DateTimeInput()
        return form_class

# custom richtextarea
class RichTextareaField(models.TextField):
    def formfield(self, **kwargs):
        form_class = super().formfield(**kwargs)
        form_class.widget = RichTextarea()
        return form_class

# custom file field that presets widget to  UploadedFileInput
def rename_upload(instance, filename):
    filename, ext = os.path.splitext(filename)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f"{uuid.uuid4().hex}_{instance.updated_by.pk}_{timestamp}{ext}"

class UploadedFileInputFormField:
    upload_to=rename_upload

    def formfield(self, **kwargs):
        form_class = super().formfield(**kwargs)
        form_class.widget = UploadedFileInput()
        return form_class

class FileField(UploadedFileInputFormField, models.FileField):
    pass

# custom image field that presets widget to  UploadedFileInput
class ImageField(UploadedFileInputFormField, models.ImageField):
    pass

class SelectizeFormField:
    def formfield(self, **kwargs):
        form_class = super().formfield(**kwargs)
        form_class.widget = Selectize()
        return form_class

class ForeignKey(SelectizeFormField, models.ForeignKey):
    pass

class OneToOne(SelectizeFormField, models.OneToOneField):
    pass

class ChoicesSelectizeFormField:
    def formfield(self, **kwargs):
        form_class = super().formfield(**kwargs)
        form_class.widget = Selectize(choices=self.choices)
        return form_class

class IntegerSelectize(ChoicesSelectizeFormField, models.IntegerField):
    pass

class TextSelectize(ChoicesSelectizeFormField, models.CharField):
    pass

# custom fields that presets to selectize multiple widget
class ManyToManyFieldSelectize(models.ManyToManyField):
    def formfield(self, **kwargs):
        form_class = super().formfield(**kwargs)
        form_class.widget = SelectizeMultiple()
        return form_class

class ManyToManyFieldDualSelector(models.ManyToManyField):
    def formfield(self, **kwargs):
        form_class = super().formfield(**kwargs)
        form_class.widget = DualSelector()
        return form_class

class RadioSelectFormField:
    def formfield(self, **kwargs):
        form_class = super().formfield(**kwargs)
        form_class.widget = forms.RadioSelect(choices=self.choices)
        return form_class

class IntegerRadioSelect(RadioSelectFormField, models.IntegerField):
    pass

class TextRadioSelect(RadioSelectFormField, models.CharField):
    pass

class BooleanRadioSelect(RadioSelectFormField, models.BooleanField):
    pass