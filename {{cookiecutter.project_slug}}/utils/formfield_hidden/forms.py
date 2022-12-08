from django import forms
from django.forms.widgets import HiddenInput


class ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if self.Meta.hidden and self.Meta.fields != "__all__":
            self.Meta.fields += self.Meta.hidden
        super().__init__(*args, **kwargs)
        try:
            for elem in self.Meta.hidden:
                self.fields[elem].widget = HiddenInput()
        except Exception as e:
            pass