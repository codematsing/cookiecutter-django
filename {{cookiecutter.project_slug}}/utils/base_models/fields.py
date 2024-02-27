"""
Custome fields that may need to be overridden due to custom default widgets
WHY DO THIS?
* To reduce requirement for custom forms when defaults are set in models

Reference: https://stackoverflow.com/questions/28497119/change-default-widgets-of-django-to-custom-ones
"""
from django.db import models
from utils.base_forms import fields

# custom date field
class DatePickerField(models.DateField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.DateFormField}
        defaults.update(kwargs)
        return super(models.DateField, self).formfield(**defaults)

# custom richtextarea
class RichTextareaField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.RichTextareaFormField}
        defaults.update(kwargs)
        return super(models.TextField, self).formfield(**defaults)

# custom file field
class FileField(models.FileField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.FileFormField}
        defaults.update(kwargs)
        return super(models.FileField, self).formfield(**defaults)

# custom file field
class ImageField(models.ImageField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.ImageFormField}
        defaults.update(kwargs)
        return super(models.ImageField, self).formfield(**defaults)

class ForeignKey(models.ForeignKey):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.ModelChoiceFormField}
        defaults.update(kwargs)
        return super(models.ForeignKey, self).formfield(**defaults)

class ManyToManyField(models.ManyToManyField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.ModelMultipleChoiceFormField}
        defaults.update(kwargs)
        return super(models.ManyToManyField, self).formfield(**defaults)