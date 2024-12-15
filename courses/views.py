from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Course
from .serializers import CourseSerializer
from .filters import CourseFilter
from .permissions import IsInstructor

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CourseFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsInstructor]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_context(self):
        return {'request': self.request}
