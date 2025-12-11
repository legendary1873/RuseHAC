"""Views for shop app."""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from .models import ShopItem, Order, PointTransaction

User = get_user_model()


class ShopItemViewSet(viewsets.ReadOnlyModelViewSet):
    """View shop items."""

    queryset = ShopItem.objects.filter(available=True)
    permission_classes = [IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    """Manage shop orders."""

    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser()])
    def award_points(self, request):
        """Award points to a user."""
        user_id = request.data.get("user_id")
        amount = request.data.get("amount")
        reason = request.data.get("reason", "Admin award")

        PointTransaction.objects.create(
            user_id=user_id, amount=amount, reason=reason, awarded_by=request.user
        )
        return Response({"status": "Points awarded"}, status=status.HTTP_201_CREATED)
