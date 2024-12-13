from rest_framework import serializers
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields=[
            'id',
            'username',
            'email',
            'password',
            'confirm_password',
            'role'
        ]

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('Passwords must match')
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_picture']
        read_only_fields = ['username', 'email']
