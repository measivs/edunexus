from rest_framework import serializers
from .models import Category, Tag


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

    def to_internal_value(self, data):
        """
        Override to handle existing and new tags gracefully.
        """
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
