#listings/filters.py
from datetime import datetime
import django_filters
from django.forms import widgets
from django.db.models import QuerySet, Q
from django.forms import TextInput, MultipleChoiceField, CheckboxInput
# from formset.widgets import SelectizeMultiple
# from formset.widgets import Selectize

from .models import ScholarshipPost

from auxiliaries.constituent_universities.models import ConstituentUniversity
from auxiliaries.year_levels.models import YearLevel
from auxiliaries.courses.models import Course
from auxiliaries.colleges.models import College
from auxiliaries.degree_levels.models import DegreeLevel
from scholarships.qualification_sets.primary_qualifications.models import ConditionEvaluator

SORT_BY_CHOICES = (
        ("title", "Title (Asc)"),
        ("-title", "Title (Desc)"),
        ("qualification_set__application_deadline", "Application deadline (Asc)"),
        ("-qualification_set__application_deadline", "Application deadline (Desc)"),
        ("qualification_set__no_slots", "Number of slots (Asc)"),
        ("-qualification_set__no_slots", "Number of slots (Desc)"),
        # ("qualification_set__no_vacant_slots", "Remaining Slots (Asc)"),
        # ("-qualification_set__no_vacant_slots", "Remaining Slots (Desc)"),
)

class ScholarshipPostFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(label='Title', lookup_expr='icontains', required=False)

    year_level = django_filters.ModelMultipleChoiceFilter(label='Year Level',
                                                          queryset=YearLevel.objects.all(),
                                                          method='evaluate_year_level',
                                                          required=False
                                                          )

    qualification_set__no_slots = django_filters.CharFilter(label='No. of Slots',
                                                           lookup_expr='lte',
                                                           widget=TextInput(attrs={'type':'number'}),
                                                           required=False)

    university = django_filters.ModelMultipleChoiceFilter(label='University',
                                                          queryset=ConstituentUniversity.objects.all(),
                                                          method='evaluate_university',
                                                          required=False)
                                                          # widget=SelectizeMultiple)

    degree_level = django_filters.ModelMultipleChoiceFilter(label='Degree Level',
                                                            queryset=DegreeLevel.objects.all(),
                                                            method='evaluate_degree_level',
                                                            required=False)
                                                            # widget=SelectizeMultiple)

    course = django_filters.ModelMultipleChoiceFilter(label='Course',
                                                      queryset=Course.objects.all(),
                                                      method='evaluate_course',
                                                      required=False)
                                                      # widget=SelectizeMultiple)

    college = django_filters.ModelMultipleChoiceFilter(label='College',
                                                       queryset=College.objects.all(),
                                                       method='evaluate_college')
                                                       # widget=SelectizeMultiple)

    gwa = django_filters.NumberFilter(label='Required GWA',
                                      method='evaluate_gwa',
                                      widget=TextInput(attrs={'type':'number'}))

    closed_applications = django_filters.BooleanFilter(label='Show open applications only',
                                                     method='evaluate_closed_applications',
                                                     widget=CheckboxInput)

    ordering = django_filters.ChoiceFilter(label="Sort by",
                                           choices=SORT_BY_CHOICES,
                                           empty_label=None,
                                           method="sort_query")

    def check_gwa(self, condition_evaluator, allowed_gwa, gwa_filter):
        if condition_evaluator == ConditionEvaluator.LessThan:
            return gwa_filter < allowed_gwa
        elif condition_evaluator == ConditionEvaluator.LessThanEqual:
            return gwa_filter <= allowed_gwa
        elif condition_evaluator == ConditionEvaluator.GreaterThan:
            return gwa_filter > allowed_gwa
        elif condition_evaluator == ConditionEvaluator.GreaterThanEqual:
            return gwa_filter >= allowed_gwa

    def _evaluate_field(self, filter_queryset, category_name, field_queryset):
        results_pk = []
        for q in filter_queryset:
            if q.qualification_set.has_primary_qualification_value(category_name, field_queryset):
                results_pk.append(q.pk)
        if results_pk:
            filter_queryset = filter_queryset.filter(pk__in=results_pk)
        return filter_queryset

    def evaluate_year_level(self, queryset, name, value):
        category_name = "year_level"
        return self._evaluate_field(queryset, category_name, value)

    def evaluate_university(self, queryset, name, value):
        category_name = "university"
        return self._evaluate_field(queryset, category_name, value)

    def evaluate_course(self, queryset, name, value):
        category_name = "course"
        return self._evaluate_field(queryset, category_name, value)

    def evaluate_college(self, queryset, name, value):
        category_name = "college"
        return self._evaluate_field(queryset, category_name, value)

    def evaluate_degree_level(self, queryset, name, value):
        category_name = "degree_level"
        return self._evaluate_field(queryset, category_name, value)

    def evaluate_gwa(self, queryset, name, gwa_filter):
        # deserialize first
        category_name = "gwa"
        results_pk = []
        for q in queryset:
            qualification = q.qualification_set.qualifications.filter(
                primaryqualification__validation_criterion__category_name=category_name
                ).first()
            primary_qualification = getattr(qualification, 'primaryqualification', None)
            if primary_qualification:
                condition_evaluator = primary_qualification.validation_criterion.condition_evaluator
                allowed_gwa = primary_qualification.deserialize_values()
                if self.check_gwa(condition_evaluator, allowed_gwa, gwa_filter):
                    results_pk.append(q.pk)

        if results_pk:
            queryset = queryset.filter(pk__in=results_pk)
        else:
            queryset = self.Meta.model.objects.none()

        return queryset

    def evaluate_closed_applications(self, queryset, name, value):
        if value == False:
            queryset = queryset.filter(Q(qualification_set__application_deadline__gte=datetime.now()))

        return queryset

    def sort_query(self, queryset, name, value):
        if value:
            # if "qualification_set__no_vacant_slots" in value:
            #     queryset = sorted(queryset, key=lambda qs: qs.qualification_set.no_vacant_slots)
            # else:
            queryset = queryset.order_by(value)
        else:
            queryset = queryset.order_by('title')

        return queryset


    class Meta:
        model = ScholarshipPost
        fields = [
                'title',
                'year_level',
                'university',
                'college',
                'degree_level',
                'course',
                'gwa',
                'qualification_set__no_slots',
                'ordering',
                'closed_applications',
                ]
