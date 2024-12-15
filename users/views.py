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

from users.models import CustomUser
from users.serializers import UserRegistrationSerializer, UserProfileSerializer, CustomTokenObtainPairSerializer, \
    VerifyEmailCodeSerializer, AddBalanceSerializer
from users.utils.email import send_verification_email, send_success_email
from users.utils.verification import generate_verification_code


# Create your views here.

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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        code_key = f"user_id_for_code_{code}"
        user_id = cache.get(code_key)

        if not user_id:
            return Response({"error": "The verification code has expired or is invalid."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        cache_key = f"verification_code_{user.id}"
        cached_code = cache.get(cache_key)

        if not cached_code or cached_code != code:
            return Response({"error": "The verification code has expired or is invalid."},
                            status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.save()
        send_success_email(user.email)

        cache.delete(cache_key)
        cache.delete(code_key)

        return Response({"message": "Verification successful! Your email has been verified."},
                        status=status.HTTP_200_OK)


class LoginUserView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileUserView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user


class AddBalanceView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddBalanceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            user_balance = request.user.balance
            user_balance.add_balance(amount)
            return Response({
                "message": "Balance added successfully!",
                "current_balance": user_balance.balance
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
