"""Views for accounts app - user auth and profile management."""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q
from .models import ExecApplication
from .serializers_new import (
    CustomTokenObtainPairSerializer,
    UserRegisterSerializer,
    UserProfileSerializer,
    ExecApplicationSerializer,
    UserListSerializer,
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view with user data."""

    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user management."""

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action == "register":
            return UserRegisterSerializer
        elif self.action == "list":
            return UserListSerializer
        return UserProfileSerializer

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Register a new user."""
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": UserProfileSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=False, methods=["put"], permission_classes=[permissions.IsAuthenticated]
    )
    def me_update(self, request):
        """Update current user profile."""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def profile(self, request, id=None):
        """Get user profile by ID (public view)."""
        user = self.get_object()
        if user.is_banned:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserListSerializer(user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def delete_account(self, request):
        """Delete current user account (leave club)."""
        user = request.user
        user.is_active = False
        user.save()
        return Response(
            {"message": "Account deactivated"}, status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def change_password(self, request):
        """Change password."""
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response(
                {"error": "Both old and new passwords required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(old_password):
            return Response(
                {"error": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated"})

    @action(detail=False, methods=["get"])
    def search(self, request):
        """Search for users by name or email."""
        query = request.query_params.get("q", "")
        if len(query) < 2:
            return Response(
                {"error": "Query too short"}, status=status.HTTP_400_BAD_REQUEST
            )

        users = User.objects.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query),
            is_active=True,
            is_banned=False,
        )[:20]
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)


class ExecApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for executive applications."""

    queryset = ExecApplication.objects.all()
    serializer_class = ExecApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def apply(self, request):
        """Apply for executive position."""
        user = request.user

        if user.role != "member":
            return Response(
                {"error": "Only members can apply"}, status=status.HTTP_400_BAD_REQUEST
            )

        if hasattr(user, "exec_application"):
            return Response(
                {"error": "You have already applied"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        statement = request.data.get("statement", "")
        if not statement or len(statement) < 50:
            return Response(
                {"error": "Statement must be at least 50 characters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        application = ExecApplication.objects.create(user=user, statement=statement)
        serializer = self.get_serializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def approve(self, request, pk=None):
        """Approve an exec application (admin only)."""
        if request.user.role not in ["admin", "exec"]:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        application = self.get_object()
        application.status = ExecApplication.Status.APPROVED
        application.reviewed_by = request.user
        application.reviewed_at = timezone.now()
        application.save()

        # Upgrade user role
        application.user.role = "exec"
        application.user.save()

        serializer = self.get_serializer(application)
        return Response(serializer.data)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def reject(self, request, pk=None):
        """Reject an exec application (admin only)."""
        if request.user.role not in ["admin", "exec"]:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        application = self.get_object()
        application.status = ExecApplication.Status.REJECTED
        application.reviewed_by = request.user
        application.reviewed_at = timezone.now()
        application.save()

        serializer = self.get_serializer(application)
        return Response(serializer.data)

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def my_application(self, request):
        """Get current user's exec application."""
        try:
            application = ExecApplication.objects.get(user=request.user)
            serializer = self.get_serializer(application)
            return Response(serializer.data)
        except ExecApplication.DoesNotExist:
            return Response(
                {"detail": "No application found"}, status=status.HTTP_404_NOT_FOUND
            )
