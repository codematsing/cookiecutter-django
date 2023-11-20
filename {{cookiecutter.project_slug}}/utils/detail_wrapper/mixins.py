from django.template.loader import render_to_string
from django.db import models
from django.contrib.auth import get_user_model
import re
import logging
logger = logging.getLogger(__name__)

class DetailWrapperMixin:
    fields = "__all__"
    card_header = "Details"
    card_subheader = ""
    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        context["fields"] = self.get_rendered_fields_items()
        context['card_header'] = self.card_header
        context['card_subheader'] = self.card_subheader
        return context

    def get_fields(self):
        if self.fields=='__all__':
            return [field.name for field in self.model._meta.fields]
        return self.fields

    def get_exclude(self):
        default = ['id', 'pk', 'created_at', 'lft', 'rght', 'tree_id', 'level', 'history']
        exclude = getattr(self, "exclude", [])
        return default+exclude

    def get_rendered_value(self, obj, field):
        field_obj = obj._meta.get_field(field)
        _field_value = getattr(obj, field, "")
        if hasattr(obj, f"render_{field}"):
            return getattr(obj, f"render{field}")()
        if isinstance(field_obj, models.ManyToManyField):
            return render_to_string('detail_wrapper/manytomany.html', {'field':_field_value})
        elif isinstance(field_obj, models.ForeignKey):
            if hasattr(_field_value, "background") or hasattr(_field_value, "foreground"):
                return render_to_string('detail_wrapper/badge.html', {'field':_field_value})
            elif type(_field_value)==get_user_model():
                return _field_value
            return render_to_string('detail_wrapper/foreignkey.html', {'field':_field_value})
        elif isinstance(field_obj, models.DateField):
            return render_to_string('detail_wrapper/date.html', {'field':_field_value})
        elif isinstance(field_obj, models.DateTimeField):
            return render_to_string('detail_wrapper/datetime.html', {'field':_field_value})
        elif isinstance(field_obj, models.EmailField):
            return render_to_string('detail_wrapper/email.html', {'field':_field_value})
        elif isinstance(field_obj, models.ImageField):
            return render_to_string('detail_wrapper/image.html', {'field':_field_value})
        elif isinstance(field_obj, models.FileField):
            if re.fullmatch(r".*\.pdf", _field_value):
                return render_to_string('detail_wrapper/pdf.html', {'field':_field_value})
            else:
                return render_to_string('detail_wrapper/file.html', {'field':_field_value})
        elif isinstance(field_obj, models.URLField):
            return render_to_string('detail_wrapper/url.html', {'field':_field_value})
        elif isinstance(field_obj, models.OneToOneField):
            return render_to_string('detail_wrapper/foreignkey.html', {'field':_field_value})
        elif hasattr(obj, f"get_{field}_display"):
            return getattr(obj, f"get_{field}_display")
        else:
            return _field_value

    def get_rendered_field_item(self, obj, field):
        if field in [field.name for field in obj._meta.fields]:
            field_obj = obj._meta.get_field(field)
            return {field_obj.verbose_name:self.get_rendered_value(obj, field)}
        else:
            return {field: getattr(obj, field, "NA")}

    def get_rendered_fields_items(self):
        obj = self.get_object()
        fields = self.get_final_fields()
        results = {}
        for field in fields:
            results.update(self.get_rendered_field_item(obj, field))
        return results

    def get_final_fields(self):
        obj = self.get_object()
        fields = self.get_fields()
        exclude = self.get_exclude()
        return list(filter(lambda field: field not in exclude, fields))

class DetailCard(DetailWrapperMixin):
    def __init__(self, object, fields, card_header="Details", card_subheader=""):
        self.object = object
        self.fields = fields
        self.card_header = card_header
        self.card_subheader = card_subheader
        self.model = self.object._meta.model

    def get_object(self):
        return self.object

    @property
    def card(self):
        return render_to_string('detail_wrapper/detail.html', context={'fields':self.get_rendered_fields_items(), 'card_header':self.card_header, 'card_subheader':self.card_subheader})