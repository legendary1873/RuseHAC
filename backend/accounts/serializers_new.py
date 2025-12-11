"""Serializers for accounts app."""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Sum
from .models import ExecApplication

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Extended token serializer with user data."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        token["name"] = f"{user.first_name} {user.last_name}"
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserProfileSerializer(self.user).data
        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "year_group",
            "password",
            "password2",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password2"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "Email already registered."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            year_group=validated_data["year_group"],
            password=validated_data["password"],
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile viewing and updating."""

    gravatar_url = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "year_group",
            "role",
            "bio",
            "gravatar_url",
            "is_banned",
            "email_notifications",
            "points",
            "created_at",
        )
        read_only_fields = (
            "id",
            "email",
            "role",
            "is_banned",
            "created_at",
            "gravatar_url",
            "points",
            "full_name",
        )

    def get_gravatar_url(self, obj):
        return obj.get_gravatar_url()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_points(self, obj):
        """Calculate total points from transactions."""
        total = obj.point_transactions.aggregate(total=Sum("amount"))["total"] or 0
        return total


class ExecApplicationSerializer(serializers.ModelSerializer):
    """Serializer for executive applications."""

    user_email = serializers.CharField(source="user.email", read_only=True)
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = ExecApplication
        fields = (
            "id",
            "user",
            "user_email",
            "user_name",
            "status",
            "statement",
            "applied_at",
            "reviewed_at",
        )
        read_only_fields = ("id", "applied_at", "reviewed_at")

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()


class UserListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing users."""

    gravatar_url = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "year_group", "role", "gravatar_url")

    def get_gravatar_url(self, obj):
        return obj.get_gravatar_url()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
