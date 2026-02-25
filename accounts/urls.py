from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, LogoutView, ProfileView, RegisterView

urlpatterns = [
    # User registration — POST with email, full_name, password, confirm_password
    path("register/", RegisterView.as_view(), name="auth-register"),

    # User login — POST with email and password → returns access + refresh tokens
    path("login/", LoginView.as_view(), name="auth-login"),

    # Token refresh — POST with refresh token → returns new access token
    path("token/refresh/", TokenRefreshView.as_view(), name="auth-token-refresh"),

    # Logout — POST with refresh token (blacklists it) — requires Auth header
    path("logout/", LogoutView.as_view(), name="auth-logout"),

    # Protected profile — GET — requires Authorization: Bearer <access_token>
    path("profile/", ProfileView.as_view(), name="auth-profile"),
]
