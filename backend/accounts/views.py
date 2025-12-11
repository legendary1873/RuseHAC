"""Views for accounts app."""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .models import ExecApplication
from .serializers import (
    UserRegisterSerializer,
    UserProfileSerializer,
    ExecApplicationSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user accounts."""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action == "create" or self.action == "register":
            return UserRegisterSerializer
        return UserProfileSerializer

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        """Register a new user."""
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def profile(self, request, id=None):
        """Get user profile by ID."""
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=["delete"], permission_classes=[IsAuthenticated])
    def delete_account(self, request):
        """Delete current user account."""
        user = request.user
        user.delete()
        return Response(
            {"message": "Account deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ExecApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for exec applications."""

    queryset = ExecApplication.objects.all()
    serializer_class = ExecApplicationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def apply(self, request):
        """Apply for executive position."""
        if hasattr(request.user, "exec_application"):
            return Response(
                {"error": "You have already applied for exec position"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ExecApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
