from rest_framework.permissions import BasePermission


class IsReviewOwner(BasePermission):
    """
    Custom permission to ensure only the review owner can update or delete the review.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user