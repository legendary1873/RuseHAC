"""Serializers for shop app."""

from rest_framework import serializers
from .models import ShopItem, Order, PointTransaction


class PointTransactionSerializer(serializers.ModelSerializer):
    """Serializer for point transactions."""

    user_email = serializers.CharField(source="user.email", read_only=True)
    awarded_by_email = serializers.CharField(
        source="awarded_by.email", read_only=True, allow_null=True
    )

    class Meta:
        model = PointTransaction
        fields = (
            "id",
            "user",
            "user_email",
            "amount",
            "reason",
            "awarded_by",
            "awarded_by_email",
            "created_at",
        )
        read_only_fields = ("id", "user", "created_at")


class ShopItemSerializer(serializers.ModelSerializer):
    """Serializer for shop items."""

    class Meta:
        model = ShopItem
        fields = (
            "id",
            "name",
            "description",
            "cost",
            "image",
            "available",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders/claims."""

    user_email = serializers.CharField(source="user.email", read_only=True)
    item_name = serializers.CharField(source="item.name", read_only=True)
    item_cost = serializers.IntegerField(source="item.cost", read_only=True)
    approved_by_email = serializers.CharField(
        source="approved_by.email", read_only=True, allow_null=True
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "user_email",
            "item",
            "item_name",
            "item_cost",
            "quantity",
            "status",
            "created_at",
            "approved_by",
            "approved_by_email",
        )
        read_only_fields = (
            "id",
            "user",
            "created_at",
            "approved_by",
            "approved_by_email",
        )
