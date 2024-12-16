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
