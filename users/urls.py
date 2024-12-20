from django.urls import path
from .views import LoginUserView, RegisterUserView, ProfileUserView, VerifyEmailCodeView, AddBalanceView, \
    GetBalanceView, PasswordResetRequestView, PasswordResetConfirmView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('verify/', VerifyEmailCodeView.as_view(), name='verify'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', ProfileUserView.as_view(), name='profile'),
    path('balance/', GetBalanceView.as_view(), name='get-balance'),
    path('balance/add/', AddBalanceView.as_view(), name='balance'),
]
