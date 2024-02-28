"""
Custome fields that may need to be overridden due to custom default widgets
WHY DO THIS?
* To reduce requirement for custom forms when defaults are set in models

Reference: https://stackoverflow.com/questions/28497119/change-default-widgets-of-django-to-custom-ones
"""
from django.db import models
from utils.base_forms import fields
from django import forms
from django.utils import timezone
import uuid
import os
import logging
logger = logging.getLogger(__name__)

# custom fields that presets to datefield widget
class DateField(models.DateField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.DateFormField}
        defaults.update(kwargs)
        return super(models.DateField, self).formfield(**defaults)

# custom fields that presets to datetimefield widget
class DateTimeField(models.DateTimeField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.DateTimeFormField}
        defaults.update(kwargs)
        return super(models.DateTimeField, self).formfield(**defaults)

# custom richtextarea
class RichTextareaField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.RichTextareaFormField}
        defaults.update(kwargs)
        return super(models.TextField, self).formfield(**defaults)

# custom file field that presets widget to  UploadedFileInput
def rename_upload(instance, filename):
    filename, ext = os.path.splitext(filename)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f"{uuid.uuid4().hex}_{instance.updated_by.pk}_{timestamp}{ext}"

class FileField(models.FileField):
    upload_to=rename_upload

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.FileFormField}
        defaults.update(kwargs)
        return super(models.FileField, self).formfield(**defaults)

# custom image field that presets widget to  UploadedFileInput
class ImageField(models.ImageField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.ImageFormField}
        defaults.update(kwargs)
        return super(models.ImageField, self).formfield(**defaults)

# custom fields that presets to selectize widget
class ForeignKey(models.ForeignKey):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.ChoiceFormField}
        defaults.update(kwargs)
        return super(models.ForeignKey, self).formfield(**defaults)

class OneToOne(models.OneToOneField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.ChoiceFormField}
        defaults.update(kwargs)
        return super(models.OneToOneField, self).formfield(**defaults)

# custom fields that presets to selectize multiple widget
class ManyToManyField(models.ManyToManyField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.MultipleChoiceFormField}
        defaults.update(kwargs)
        return super(models.ManyToManyField, self).formfield(**defaults)

class IntegerChoiceField(models.IntegerField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.ChoiceFormField}
        defaults.update(kwargs)
        return super(models.IntegerField, self).formfield(**defaults)

class TextChoiceField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.ChoiceFormField}
        defaults.update(kwargs)
        return super(models.CharField, self).formfield(**defaults)