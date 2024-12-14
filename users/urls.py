from django.urls import path, include
from .views import LoginUserView, RegisterUserView, ProfileUserView, VerifyEmailCodeView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify/', VerifyEmailCodeView.as_view(), name='verify'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', ProfileUserView.as_view(), name='profile'),
]
