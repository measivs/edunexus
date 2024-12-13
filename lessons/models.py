from django.db import models

# Create your models here.

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='lessons')
    video = models.FileField(upload_to="lessons/videos/", blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
