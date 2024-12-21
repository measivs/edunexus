from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name="orders")
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name="orders")
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - {self.status}"

    # def mark_completed(self):
    #     """Mark the order as completed."""
    #     self.status = 'completed'
    #     self.save()
    #
    # def mark_failed(self):
    #     """Mark the order as failed."""
    #     self.status = 'failed'
    #     self.save()
    #
    # def mark_cancelled(self):
    #     """Mark the order as cancelled."""
    #     self.status = 'cancelled'
    #     self.save()
    #
    # @classmethod
    # def user_has_ordered(cls, user, course):
    #     return cls.objects.filter(user=user, course=course).exists()


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2,
                                              help_text="Enter a value between 1 and 100")
    valid_until = models.DateTimeField(help_text="Coupon expiry date")
    is_active = models.BooleanField(default=True)

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_coupons")
    courses = models.ManyToManyField('courses.Course', blank=True, related_name="applicable_coupons",
                                     help_text="Leave empty for global coupon")
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                          help_text="Minimum order amount required to use this coupon.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notified = models.BooleanField(default=False, help_text="Set to True if expiry email was sent.")

    def is_valid(self):
        """Check if a coupon is active and not expired."""
        return self.is_active and timezone.now() < self.valid_until

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"
