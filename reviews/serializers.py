from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from courses.models import Course
from reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    course = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'user', 'course', 'created_at']
        read_only_fields = ['id', 'user', 'course', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        course_pk = self.context['view'].kwargs.get('course_pk')
        course = Course.objects.get(pk=course_pk)
        if course.instructor == user:
            raise ValidationError("Instructors cannot write reviews for their own courses.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        course_pk = self.context['view'].kwargs.get('course_pk')
        if not course_pk:
            raise KeyError("course_pk is required in the context for creating reviews.")
        course = Course.objects.get(pk=course_pk)
        validated_data.pop('user', None)
        validated_data.pop('course', None)
        return Review.objects.create(user=user, course=course, **validated_data)
