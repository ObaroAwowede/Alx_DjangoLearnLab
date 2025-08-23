from django.contrib import admin
from django.urls import path
from .views import RegisterView, LoginView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register-view'),
    path('login/', LoginView.as_view(), name = 'login-view'),
    path('profile/', ProfileView.as_view(), name = 'profile-view'),
]