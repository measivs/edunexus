from django.urls import path, include
from .views import LoginUserView, RegisterUserView, ProfileUserView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', ProfileUserView.as_view(), name='profile'),
]
