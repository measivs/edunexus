from django.db import models

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='orders')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='orders')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
