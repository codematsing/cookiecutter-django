from django import forms
from utils.base_forms.forms import BaseFormCollection, BaseModelForm
from unit_roles.models import UnitRole
from django.core.exceptions import NON_FIELD_ERRORS
from formset.renderers.bootstrap import FormRenderer
import pandas as pd
import logging
logger = logging.getLogger(__name__)

class UnitRoleForm(BaseModelForm):
    default_renderer = FormRenderer(
        # collection_css_classes = "card",
        # fieldset_css_classes="border rounded p-3",
        form_css_classes='row mt-0 mb-4 py-4 px-2 shadow rounded-3',
		fieldset_css_classes="row",
        field_css_classes={
            '*': 'mb-2 col-sm-12 col-md-6',
        },
    )
    is_primary = forms.BooleanField(
        label="Select as Primary Unit Role",
        required=False,
        initial=False
    )
    class Meta:
        model = UnitRole
        fields = ['unit', 'role']

class UnitRoleFormset(BaseFormCollection):
    legend = "Unit Roles"
    min_siblings = 0
    unit_role_form = UnitRoleForm()

    def full_clean(self):
        super().full_clean()
        df = pd.json_normalize(self.cleaned_data)
        logger.info(df["unit_role_form.is_primary"].sum())
        if df['unit_role_form.is_primary'].sum() > 1:
            self._errors[0]['unit_role_form'][NON_FIELD_ERRORS] = ["Please select only one primary Unit Role"]