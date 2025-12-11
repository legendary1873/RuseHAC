"""Serializers for accounts app."""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ExecApplication

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "year_group", "password")

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
    gravatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "year_group",
            "role",
            "bio",
            "gravatar_url",
            "is_banned",
            "email_notifications",
            "created_at",
        )
        read_only_fields = ("id", "role", "is_banned", "created_at", "gravatar_url")

    def get_gravatar_url(self, obj):
        return obj.get_gravatar_url()


class ExecApplicationSerializer(serializers.ModelSerializer):
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
        return f"{obj.user.first_name} {obj.user.last_name}"
