from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Enrollment
from orders.models import Order
from .permissions import IsInstructor
from .serializers import CourseSerializer, EnrollmentSerializer
from .filters import CourseFilter

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CourseFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsInstructor]
        elif self.action == 'enroll':
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated], serializer_class=EnrollmentSerializer)
    def enroll(self, request, pk=None):
        course = self.get_object()
        user = request.user

        if not Order.objects.filter(user=user, course=course, status='completed').exists():
            return Response({'status': 'order not found or not completed'}, status=status.HTTP_400_BAD_REQUEST)

        if Enrollment.objects.filter(user=user, course=course).exists():
            return Response({'status': 'already enrolled'}, status=status.HTTP_400_BAD_REQUEST)

        Enrollment.objects.create(user=user, course=course)

        return Response({'status': 'user enrolled'}, status=status.HTTP_200_OK)
