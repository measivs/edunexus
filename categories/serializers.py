from rest_framework import serializers
from .models import Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    """
        Serializer for representing and managing category data.

        Fields:
            - `name` (str): The name of the category.
            - `description` (str): Optional description of the category.
            - `parent` (int): Reference to a parent category, allowing hierarchical organization.

        Functionality:
            - Supports hierarchical category structures using the `parent` field.
            - Handles both existing and new category data gracefully.

        Overrides:
            - `to_internal_value`: Ensures that if a category with the provided name exists,
              it is returned instead of attempting to recreate it.
    """
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
    """
        Serializer for representing and managing tag data.

        Fields:
            - `name` (str): The name of the tag.

        Functionality:
            - Ensures that tags can be created or linked seamlessly.
            - Handles both new and existing tags gracefully.

        Overrides:
            - `to_internal_value`: Processes tag data to check if it refers to an existing tag.
              If the tag exists, it is returned instead of creating a duplicate.
    """
    class Meta:
        model = Tag
        fields = ['name']

    def to_internal_value(self, data):
        if isinstance(data, dict):
            name = data.get('name')
            if not name:
                raise serializers.ValidationError({"name": "This field is required."})
            try:
                tag = Tag.objects.get(name=name)
                return tag
            except Tag.DoesNotExist:
                return super().to_internal_value(data)

        raise serializers.ValidationError("Invalid data format for Tag.")
