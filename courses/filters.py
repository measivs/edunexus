import django_filters
from .models import Course


class CourseFilter(django_filters.FilterSet):
    """
        Custom filter for courses.

        Features:
            - Filters courses based on title, category, instructor, tags, and minimum rating.

        Fields:
            - `title`: Filters courses containing the title (case-insensitive).
            - `category`: Filters courses based on their category name.
            - `instructor`: Filters courses by the instructor's username.
            - `tags`: Filters courses based on tags.
            - `min_rating`: Filters courses with an average rating equal to or above the given value.

        Methods:
            - `filter_tags`: Filters courses that include specific tags.
            - `filter_min_rating`: Filters courses based on a minimum average rating.
    """
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    instructor = django_filters.CharFilter(field_name='instructor__username', lookup_expr='icontains')
    tags = django_filters.CharFilter(method='filter_tags')
    min_rating = django_filters.NumberFilter(method='filter_min_rating')

    class Meta:
        model = Course
        fields = ['title', 'category', 'instructor', 'tags', 'min_rating']

    def filter_tags(self, queryset, name, value):
        tag_names = value.split(',')
        return queryset.filter(tags__name__in=tag_names).distinct()

    def filter_min_rating(self, queryset, name, value):
        return queryset.filter(id__in=[
            course.id for course in queryset if course.average_rating() and course.average_rating() >= value
        ])
