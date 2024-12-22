from django.dispatch import Signal, receiver

from courses.models import Enrollment


order_success = Signal()
"""
Signal to broadcast upon successful course purchase.

Broadcasts:
    - `user`: The user who purchased the course.
    - `course`: The course that was purchased.
"""


@receiver(order_success)
def enroll_user_after_order(sender, **kwargs):
    """
    Signal receiver to enroll a user in a course after a successful purchase.

    Args:
        sender: The model class that sent the signal.
        user: The user who purchased the course (required).
        course: The purchased course (required).

    Behavior:
        - Automatically enrolls the user in the course if not already enrolled.
        - Handles cases where enrollment already exists or data is missing.
    """
    user = kwargs.get('user')
    course = kwargs.get('course')

    if not user or not course:
        return

    if not Enrollment.objects.filter(user=user, course=course).exists():
        Enrollment.objects.create(user=user, course=course)
        print(f"User {user.username} has been enrolled in the course: {course.title}.")
    else:
        print(f"User {user.username} is already enrolled in the course: {course.title}.")
