from rest_framework import serializers
from .models import Course, Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Category
        fields = ['name', 'description', 'parent']

    def to_internal_value(self, data):
        name = data.get('name')
        try:
            category = Category.objects.get(name=name)
            return category
        except Category.DoesNotExist:
            return super().to_internal_value(data)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'title', 'description', 'category', 'tags',
            'created_at', 'average_rating'
        ]

    def create(self, validated_data):
        category = validated_data.pop('category')
        tags = validated_data.pop('tags')
        instructor = self.context['request'].user
        course = Course.objects.create(instructor=instructor, category=category, **validated_data)

        for tag_data in tags:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            course.tags.add(tag)

        return course

    def update(self, instance, validated_data):
        category = validated_data.pop('category')
        tags = validated_data.pop('tags')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.category = category
        instance.save()

        instance.tags.clear()
        for tag_data in tags:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            instance.tags.add(tag)

        return instance


class EnrollmentSerializer(serializers.Serializer):
    pass
