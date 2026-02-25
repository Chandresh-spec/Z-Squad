from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import User
from .serializers import LoginSerializer, RegisterSerializer, UserProfileSerializer


def get_tokens_for_user(user):
    """
    Generate a pair of JWT access and refresh tokens for a given user.
    Returns a dict with 'refresh' and 'access' keys.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class RegisterView(APIView):
    """
    POST /api/auth/register/
    Creates a new user account. Open to all (no auth required).

    Request Body:
        {
            "email": "user@example.com",
            "full_name": "John Doe",
            "password": "strongpass123",
            "confirm_password": "strongpass123"
        }
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    "message": "Account created successfully.",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "full_name": user.full_name,
                    },
                    "tokens": tokens,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    POST /api/auth/login/
    Authenticates a user with email + password and returns JWT tokens.

    Request Body:
        {
            "email": "user@example.com",
            "password": "strongpass123"
        }
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    "message": "Login successful.",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "full_name": user.full_name,
                    },
                    "tokens": tokens,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Blacklists the provided refresh token, effectively logging the user out.
    Requires a valid access token in the Authorization header.

    Request Body:
        {
            "refresh": "<refresh_token>"
        }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logged out successfully."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except TokenError as e:
            return Response(
                {"error": f"Invalid or expired token: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProfileView(APIView):
    """
    GET /api/auth/profile/
    Returns the profile of the currently authenticated user.
    Requires Authorization: Bearer <access_token> header.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(
            {
                "message": "Profile fetched successfully.",
                "user": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
