from rest_framework import serializers
from categories.models import Category, Tag
from .models import Course, Enrollment, Lesson
from categories.serializers import TagSerializer


class CourseSerializer(serializers.ModelSerializer):
    """
        Serializer for representing and managing course details.

        Fields:
            - `id`: Unique identifier of the course.
            - `title`: Title of the course.
            - `description`: Description of the course content.
            - `category`: Category of the course (linked by name).
            - `tags`: Tags associated with the course (optional).
            - `price`: Price of the course (mandatory).

        Validations:
            - Ensures the provided category exists.
            - Ensures unique tags are created or linked to the course.

        Methods:
            - `validate_category`: Validates and fetches categorized information by name.
            - `create`: Creates a course with associated tags and instructor details.
            - `update`: Updates course information and tags.
    """
    category = serializers.CharField(
        write_only=True,
        help_text="Select an existing category (admins create categories).",
    )
    tags = TagSerializer(many=True, required=False)
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'tags', 'price']

    def validate_category(self, value):
        try:
            category = Category.objects.get(name=value)
            return category
        except Category.DoesNotExist:
            raise serializers.ValidationError(f"Category '{value}' does not exist. Please select an existing category.")

    def create(self, validated_data):
        category_name = validated_data.pop('category')
        tags_data = validated_data.pop('tags', [])
        instructor = self.context['request'].user
        category = Category.objects.get(name=category_name)
        course = Course.objects.create(instructor=instructor, category=category, **validated_data)
        for tag_data in tags_data:
            if isinstance(tag_data, Tag):
                course.tags.add(tag_data)
            elif isinstance(tag_data, dict) and 'name' in tag_data:
                tag, _ = Tag.objects.get_or_create(name=tag_data['name'])
                course.tags.add(tag)
        return course

    def update(self, instance, validated_data):
        category_name = validated_data.pop('category', None)
        tags_data = validated_data.pop('tags', [])
        if category_name:
            category = Category.objects.get(name=category_name)
            instance.category = category
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        instance.tags.clear()

        for tag_data in tags_data:
            if isinstance(tag_data, Tag):
                instance.tags.add(tag_data)
            elif isinstance(tag_data, dict) and 'name' in tag_data:
                tag, _ = Tag.objects.get_or_create(name=tag_data['name'])
                instance.tags.add(tag)
        return instance


class EnrollmentSerializer(serializers.ModelSerializer):
    """
        Serializer for representing enrollment details.

        Fields:
            - `course`: Associated course (including nested details).
            - `enrolled_at`: Timestamp of when the user enrolled.
            - `progress`: Progress made by the user in the course.
            - `completed`: Indicates if the course is completed.
    """
    course = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = ['course', 'enrolled_at', 'progress', 'completed']


class LessonSerializer(serializers.ModelSerializer):
    """
        Serializer for managing lesson details.

        Fields:
            - `id`: Unique identifier of the lesson.
            - `title`: Title of the lesson.
            - `course`: Course the lesson belongs to.
            - `video`: Optional video file for the lesson.
            - `content`: Text content of the lesson.
            - `created_at`: Timestamp of when the lesson was created.

        Read-only Fields:
            - `id` and `created_at`.
    """
    video = serializers.FileField(
        allow_null=True,
        required=False,
        help_text="Upload a video file (e.g., MP4 format)"
    )

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'course', 'video', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']


class PopularCourseSerializer(serializers.ModelSerializer):
    """
        Serializer for retrieving popular course details.

        Fields:
            - `id`: Unique identifier of the course.
            - `title`: Title of the course.
            - `description`: Description of the course.
            - `instructor`: The instructor who created the course.
            - `price`: Price of the course.
            - `category`: Associated category of the course.
            - `enrollment_count`: Number of enrollments in the course (read-only).
    """
    enrollment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'price', 'category', 'enrollment_count']
