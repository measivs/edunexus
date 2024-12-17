from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from categories.models import Category
from categories.serializers import CategorySerializer
from courses.models import Course
from courses.serializers import CourseSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for managing categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'courses']:
            return [AllowAny()]
        return [IsAdminUser()]

    @action(detail=True, methods=['get'], url_path='courses')
    def courses(self, request, pk=None):
        """
        Custom endpoint to fetch all courses related to a specific category.
        """
        try:
            category = self.get_object()
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        courses = Course.objects.filter(category=category)
        serializer = CourseSerializer(courses, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
