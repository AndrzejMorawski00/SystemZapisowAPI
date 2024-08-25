import django_filters

from panel.models import Course, CourseTag, CourseEffect

class CourseFilter(django_filters.FilterSet):
    type = django_filters.NumberFilter(field_name='type')
    tags = django_filters.ModelMultipleChoiceFilter(queryset=CourseTag.objects.all(), conjoined=True)
    effects = django_filters.ModelMultipleChoiceFilter(queryset=CourseEffect.objects.all(), conjoined=True)
    recommended_for_first_year = django_filters.BooleanFilter('recommended_for_first_year')

    class Meta:
        model = Course
        fields = ['type', 'tags', 'effects', 'recommended_for_first_year']
    




