from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CourseViewSet

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
]
