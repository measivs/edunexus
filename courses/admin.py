from django.contrib import admin

from courses.models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    pass
