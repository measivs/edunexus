from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Review, Course
from .permissions import IsReviewOwner
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwner]

    def get_queryset(self):
        course_id = self.kwargs.get('course_pk')
        if course_id:
            return Review.objects.filter(course_id=course_id)
        return Review.objects.none()

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_pk')
        if not course_id:
            raise KeyError("course_pk is required in the URL for creating a review.")
        course = Course.objects.get(pk=course_id)
        serializer.save(course=course, user=self.request.user)
