from django.db import models
from colorfield.fields import ColorField

# Create your models here.

class BaseTag(models.Model):
    name = models.name = models.CharField(max_length=64, blank=False, null=False)
    color = ColorField(default='#006dad')

    class Meta:
        abstract = True