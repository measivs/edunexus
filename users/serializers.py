from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import CustomUser

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
        Serializer for registering new users.

        Validates passwords and ensures that they match before creating the user account.
    """
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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
        Customized serializer for obtaining JWT tokens.

        Ensures that only verified users can log in and obtain tokens.
    """
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_verified:
            raise ValidationError("Your email is not verified.")

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """
        Serializer for viewing and updating user profiles.

        Includes fields such as username, email, bio, and profile picture.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_picture']
        read_only_fields = ['username', 'email']


class VerifyEmailCodeSerializer(serializers.Serializer):
    """
        Serializer for verifying an email code.

        Requires a 6-digit code to complete the email verification process.
    """
    code = serializers.CharField(max_length=6)


class BalanceSerializer(serializers.Serializer):
    """
        Serializer for displaying the user's current balance.

        Provides the `balance` as a floating-point value.
    """
    balance = serializers.FloatField()


class AddBalanceSerializer(serializers.Serializer):
    """
        Serializer for adding funds to the user's account balance.

        Validates that the amount to be added is positive.
    """
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """
        Serializer for requesting a password reset.

        Validates the provided email and ensures it belongs to an existing user.
    """
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("There is no user registered with this email.")
        return email


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
        Serializer to validate and confirm the password reset process.

        Verifies the token and updates the user's password upon successful validation.
    """
    token = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        email = data['email']
        token = data['token']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Invalid email."})

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise serializers.ValidationError({"token": "Invalid or expired token."})

        return data

    def save(self):
        email = self.validated_data['email']
        password = self.validated_data['password']

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return user
