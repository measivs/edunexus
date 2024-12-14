from django.contrib.auth import get_user_model
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserRegistrationSerializer, UserProfileSerializer, CustomTokenObtainPairSerializer, \
    VerifyEmailCodeSerializer
from users.utils.email import send_verification_email, send_success_email
from users.utils.verification import generate_verification_code


# Create your views here.

User = get_user_model()


class RegisterUserView(GenericAPIView):
    """
    Registers a user and sends a verification code via email.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        code = generate_verification_code(user.id)

        send_verification_email(user.email, code)

        return Response({
            "message": "User registered successfully. A verification code has been sent to your email.",
            "user_id": user.id,
        }, status=status.HTTP_201_CREATED)


class VerifyEmailCodeView(GenericAPIView):
    """
    Verifies the code sent to the user's email address.
    """
    serializer_class = VerifyEmailCodeSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user_id = request.data.get("user_id")
        code = request.data.get("code")
        cache_key = f"verification_code_{user_id}"
        cached_code = cache.get(cache_key)

        if not cached_code:
            return Response({"error": "The verification code has expired or is invalid."},
                            status=status.HTTP_400_BAD_REQUEST)

        if cached_code == code:
            try:
                user = User.objects.get(id=user_id)
                user.is_verified = True
                user.save()
                send_success_email(user.email)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            cache.delete(cache_key)
            return Response({"message": "Verification successful! Your email has been verified."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "Incorrect verification code."}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileUserView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user

