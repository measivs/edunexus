import django_filters
from .models import Course


class CourseFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')  # Add this to filter by title
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    instructor = django_filters.CharFilter(field_name='instructor__username', lookup_expr='icontains')
    tags = django_filters.CharFilter(method='filter_tags')
    min_rating = django_filters.NumberFilter(method='filter_min_rating')

    class Meta:
        model = Course
        fields = ['title', 'category', 'instructor', 'tags', 'min_rating']  # Add `title` to the fields list

    def filter_tags(self, queryset, name, value):
        tag_names = value.split(',')
        return queryset.filter(tags__name__in=tag_names).distinct()

    def filter_min_rating(self, queryset, name, value):
        return queryset.filter(id__in=[
            course.id for course in queryset if course.average_rating() and course.average_rating() >= value
        ])
