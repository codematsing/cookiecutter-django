from utils.base_forms.forms import BaseModelForm, BaseFormCollection
from django import forms
from faqs.models import FaqItem
from formset.richtext.widgets import RichTextarea

class FaqItemForm(BaseModelForm):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    class Meta:
        model = FaqItem
        exclude = ['order']
        widgets = {
            "answer": RichTextarea(),
            "is_published": forms.RadioSelect(),
        }

class FaqCollectionForm(BaseFormCollection):
    faq_item_form = FaqItemForm()
    min_siblings = 1
    add_label = "Add Faq"
    is_sortable = True

    def save(self):
        cleaned_data = self.clean()
        for index, faq_item in enumerate(cleaned_data):
            faq_item_kwargs = faq_item['faq_item_form']
            id = faq_item_kwargs.pop('id', None)
            request_to_remove_item = faq_item_kwargs.pop('_marked_for_removal_', False)
            if request_to_remove_item and id:
                FaqItem.objects.filter(id=id).delete()
            else:
                faq_item_kwargs['order'] = index
                FaqItem.objects.update_or_create(id=id, defaults=faq_item_kwargs)