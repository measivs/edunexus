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
from orders.models import Order
from .permissions import IsInstructor, IsCourseOwner
from .serializers import CourseSerializer, EnrollmentSerializer, LessonSerializer, PopularCourseSerializer
from .filters import CourseFilter

class CourseViewSet(ModelViewSet):
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

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated],
            serializer_class=EnrollmentSerializer)
    def enroll(self, request, pk=None):
        course = self.get_object()
        user = request.user

        if not Order.objects.filter(user=user, course=course, status='completed').exists():
            return Response({'status': 'order not found or not completed'}, status=status.HTTP_400_BAD_REQUEST)

        if Enrollment.objects.filter(user=user, course=course).exists():
            return Response({'status': 'already enrolled'}, status=status.HTTP_400_BAD_REQUEST)

        Enrollment.objects.create(user=user, course=course)

        return Response({'status': 'user enrolled'}, status=status.HTTP_200_OK)

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
    permission_classes = [AllowAny]

    def get(self, request):
        popular_courses = Course.objects.annotate(
            enrollment_count=Count('enrollments')
        ).order_by('-enrollment_count')

        serializer = PopularCourseSerializer(popular_courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
