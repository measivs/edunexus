from django.contrib import admin
from courses.models import Course, Enrollment, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'instructor', 'category', 'price', 'created_at')
    list_filter = ('category', 'created_at', 'price')
    search_fields = ('title', 'description', 'instructor__username')
    ordering = ('created_at',)
    prepopulated_fields = {'title': ('description',)}
    list_editable = ('price',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'enrolled_at', 'progress', 'completed')
    list_filter = ('completed', 'enrolled_at')
    search_fields = ('user__username', 'course__title')
    ordering = ('enrolled_at',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'course__title')
    ordering = ('created_at',)
