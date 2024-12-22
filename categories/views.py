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
        A ModelViewSet for managing categories in the application.

        Features:
            - Supports all CRUD operations for categories (create, retrieve, update, delete).
            - Allows users to filter and search categories by name.
            - Provides a custom endpoint for fetching courses within a specific category.

        Attributes:
            - `queryset`: Queryset for retrieving all categories.
            - `serializer_class`: Serializer class associated with categories.
            - `filter_backends`: Backends used for filtering and searching.
            - `search_fields`: Specifies fields to be searched (name).
            - `filterset_fields`: Specifies fields to be used for filtering (name).

        Methods:
            - `get_permissions`: Dynamically determines permissions based on the action.
            - Any user can list or retrieve categories and fetch their courses.
            - Only admin users can create, update, or delete categories.
            - `courses`: A custom action to fetch all courses that belong to a specific category.
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
        try:
            category = self.get_object()
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        courses = Course.objects.filter(category=category)
        serializer = CourseSerializer(courses, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
