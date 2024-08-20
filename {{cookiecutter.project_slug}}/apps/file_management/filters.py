import django_filters

from .models import ScholarshipPost

class ScholarshipPostFilter(django_filters.FilterSet):
    class Meta:
        model = ScholarshipPost
        fields = 
