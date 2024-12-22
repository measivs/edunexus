from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Review, Course
from .permissions import IsReviewOwner
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    """
        A viewset for managing course reviews.

        Features:
            - Supports Create, Read (List/Retrieve), Update, and Delete actions for reviews.
            - Filters the queryset based on the course's
              primary key (`course_pk`) provided in the URL.
            - Ensures only authenticated users can create/update reviews
              and only review owners can modify or delete their reviews.

        Permissions:
            - `IsAuthenticatedOrReadOnly`: Allows authenticated users
               to create or modify reviews and unauthenticated users to only view reviews.
            - `IsReviewOwner`: Restricts modification or deletion to the owner of the review.

        Methods:
            - `get_queryset`: Filters reviews for the specific
               course based on `course_pk` provided in the URL.
            - `perform_create`: Handles review creation, linking it to
               the course and the user who created the review.
    """
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
