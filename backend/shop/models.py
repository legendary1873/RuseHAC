"""Models for shop app."""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PointTransaction(models.Model):
    """Record of point transactions."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="point_transactions"
    )
    amount = models.IntegerField()
    reason = models.CharField(max_length=255)
    awarded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="awarded_points",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.amount} points"


class ShopItem(models.Model):
    """Item available in the shop."""

    name = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.IntegerField()  # In points
    image = models.ImageField(upload_to="shop_items/")
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    """User order/claim for shop items."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        CLAIMED = "claimed", "Claimed"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_orders",
    )

    def __str__(self):
        return f"{self.user.email} - {self.item.name}"
