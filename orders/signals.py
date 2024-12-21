from django.dispatch import Signal, receiver

from courses.models import Enrollment

# Signal to fire after a successful course purchase
order_success = Signal()


@receiver(order_success)
def enroll_user_after_order(sender, **kwargs):
    """
    Signal receiver to automatically enroll the user in a course after a successful purchase.
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
