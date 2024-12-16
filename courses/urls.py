from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import CourseViewSet, LessonViewSet
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

courses_router = NestedSimpleRouter(router, r'courses', lookup='course')
courses_router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
]
