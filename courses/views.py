from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

from .models import Course, Enrollment, Lesson
from .permissions import IsInstructor, IsCourseOwner
from .serializers import CourseSerializer, EnrollmentSerializer, LessonSerializer, PopularCourseSerializer
from .filters import CourseFilter

class CourseViewSet(ModelViewSet):
    """
        ViewSet for managing courses.

        Features:
            - Handles CRUD operations for courses.
            - Includes filtering, enrolling users, and listing course enrollments.

        Methods:
            - `get_permissions`: Determines permissions dynamically for different actions.
            - `list_enrollments`: Lists enrollments of users in a course.
            - `retrieve_enrollment`: Retrieves details of a specific enrollment.
            - `list`: Lists available courses with optional filters.

        Attributes:
            - `queryset`: Default queryset for courses.
            - `serializer_class`: Serializer class associated with courses.
            - `filter_backends`: Backends to handle filtering mechanics.
            - `filterset_class`: Filter set class for course filtering.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CourseFilter

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated, IsInstructor]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsInstructor, IsCourseOwner]
        elif self.action in ['enroll', 'list_enrollments', 'retrieve_enrollment']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def list_enrollments(self, request):
        user = request.user
        cache_key = f"user_enrollments_{user.id}"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        enrollments = Enrollment.objects.filter(user=user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        cache.set(cache_key, serializer.data, timeout=60*15)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def retrieve_enrollment(self, request, pk=None):
        enrollment = Enrollment.objects.filter(user=request.user, course__pk=pk).first()
        if not enrollment:
            return Response({'detail': 'Enrollment not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        cached_courses = cache.get('course_list')
        if cached_courses is not None:
            return Response(cached_courses)

        response = super().list(request, *args, **kwargs)
        cache.set('course_list', response.data, timeout=60*15)
        return response


class LessonViewSet(ModelViewSet):
    """
        ViewSet for managing lessons within courses.

        Features:
            - Handles CRUD operations for lessons.
            - Supports file uploads for lessons (e.g., video files).

        Methods:
            - `get_permissions`: Determines permissions dynamically for different actions.
            - `get_queryset`: Retrieves lessons related to a specific course.
            - `perform_create`: Handles lesson creation, associating it with a course.

        Attributes:
            - `serializer_class`: Serializer class associated with lessons.
            - `parser_classes`: Parsers supported for request data handling.
    """
    serializer_class = LessonSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsInstructor]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        return Lesson.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_pk']
        serializer.save(course_id=course_id)


class PopularCoursesView(GenericAPIView):
    """
        View for retrieving a list of popular courses.

        Features:
            - Lists courses sorted by popularity (e.g., enrollment count).

        Methods:
            - `get`: Returns a query set of popular courses sorted by specified criteria.

        Attributes:
            - `permission_classes`: Permissions applied to accessing this view.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        popular_courses = Course.objects.annotate(
            enrollment_count=Count('enrollments')
        ).order_by('-enrollment_count')

        serializer = PopularCourseSerializer(popular_courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
