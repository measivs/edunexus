from rest_framework import serializers

from .models import Course, Enrollment, Lesson
from categories.serializers import CategorySerializer, TagSerializer


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'tags']

    def create(self, validated_data):
        """
        Override create method to handle category and tags properly.
        """
        category_data = validated_data.pop('category')
        tags_data = validated_data.pop('tags')
        instructor = self.context['request'].user
        course = Course.objects.create(instructor=instructor, category=category_data, **validated_data)

        for tag in tags_data:
            course.tags.add(tag)

        return course

    def update(self, instance, validated_data):
        """
        Override update method to handle category and tags properly.
        """
        category_data = validated_data.pop('category')
        tags_data = validated_data.pop('tags')

        instance.category = category_data
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        instance.tags.clear()
        for tag in tags_data:
            instance.tags.add(tag)

        return instance


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = ['course', 'enrolled_at', 'progress', 'completed']


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.FileField(
        allow_null=True,
        required=False,
        help_text="Upload a video file (e.g., MP4 format)"
    )

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'course', 'video', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']
