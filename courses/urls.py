from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from reviews.views import ReviewViewSet
from .views import CourseViewSet, LessonViewSet, PopularCoursesView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

courses_router = NestedSimpleRouter(router, r'courses', lookup='course')
courses_router.register(r'lessons', LessonViewSet, basename='lesson')
courses_router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('courses/popular-courses/', PopularCoursesView.as_view(), name='popular-courses'),
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
]
