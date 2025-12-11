"""Admin for shop app."""

from django.contrib import admin
from .models import ShopItem, Order, PointTransaction


@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    list_display = ("name", "cost", "available")
    list_filter = ("available",)
    search_fields = ("name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__email", "item__name")


@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "reason", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__email", "reason")
