from django.db import models

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey('categories.Category', on_delete=models.SET_NULL, null=True, related_name='courses')
    tags = models.ManyToManyField('categories.Tag', related_name='courses', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return None


class Enrollment(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lessons')
    video = models.FileField(upload_to="lessons/videos/", blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title