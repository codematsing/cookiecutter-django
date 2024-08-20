from django import forms
from formset.widgets import SelectizeMultiple, DateTimeInput
from utils.base_forms.forms import CustomSelectizeMultiple, ImageFileWidget
from formset.richtext.widgets import RichTextarea
from auxiliaries.constituent_universities.models import ConstituentUniversity
from auxiliaries.year_levels.models import YearLevel
from auxiliaries.courses.models import Course
from utils.base_forms.forms import BaseModelForm
from formset.renderers.bootstrap import FormRenderer
from utils.lambdas import TF_BOOLEAN_CHOICES
from .models import Post

SORT_BY_CHOICES = (
	("title", "Title (Asc)"),
	("-title", "Title (Desc)"),
	("qualification_set__application_deadline", "Application deadline (Asc)"),
	("-qualification_set__application_deadline", "Application deadline (Desc)"),
	("qualification_set__no_slots", "Number of slots (Asc)"),
	("-qualification_set__no_slots", "Number of slots (Desc)"),
)

FILTER_FIELD_CLASSES = {
		'title': 'col-md-4',
		'constituent_university': 'col-md-4',
		'course': 'col-md-4',
		'year_level': 'col-md-4',
		'overall_gwa': 'col-md-4',
		'no_slots': 'col-md-4',
		'order_by': 'col-md-4',
		'closed_applications': 'col-md-4',
		'qualified_applications': 'col-md-4',
}

class FilterForm(forms.Form):
	default_renderer = FormRenderer(
		form_css_classes="row",
		fieldset_css_classes="row",
		field_css_classes =  FILTER_FIELD_CLASSES,
	)
	field_order = FILTER_FIELD_CLASSES.keys()

	title = forms.CharField(
		label="Title contains",
		required=False,
	)

	no_slots = forms.CharField(
		label="Avail. slots at least",
		widget=forms.TextInput(attrs={"type": "number"}),
		required=False,
	)

	overall_gwa = forms.CharField(
		label="Must accept GWA", widget=forms.TextInput(attrs={"type": "number"}),
		required=False
	)

	closed_applications = forms.BooleanField(
		label="Show past applications", initial=True, required=False,
	)

	qualified_applications = forms.BooleanField(
		label="Show only scholarships that apply to me", initial=False, required=False,
		help_text="Requires portfolio accomplished"
	)

	year_level = forms.ModelMultipleChoiceField(
		label="Accepts year level",
		queryset=YearLevel.objects.all(),
		required=False,
		widget=SelectizeMultiple,
	)

	constituent_university = forms.ModelMultipleChoiceField(
		label="Avail. for campus",
		queryset=ConstituentUniversity.objects.all(),
		required=False,
		widget=SelectizeMultiple,
	)

	course = forms.ModelMultipleChoiceField(
		label="Avail. for courses",
		queryset=Course.objects.all(),
		required=False,
		widget=CustomSelectizeMultiple,
	)

	order_by = forms.ChoiceField(
		label="Sort by", choices=SORT_BY_CHOICES, initial="-qualification_set__application_deadline"
	)

class PostForm(BaseModelForm):
	legend = "Scholarship Post Details"
	body = forms.CharField(widget=RichTextarea(), required=False)

	class Meta:
		model = Post
		exclude = ['published_date']
		widgets = {
			'thumbnail': ImageFileWidget(),
			'is_published': forms.RadioSelect(),
			'tags': SelectizeMultiple(),
		}
