"""Views for shop app - points and merchandise."""

from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Sum
from .models import ShopItem, Order, PointTransaction
from .serializers import ShopItemSerializer, OrderSerializer, PointTransactionSerializer

User = get_user_model()


class IsExecOrReadOnly(permissions.BasePermission):
    """Execs can manage, everyone can view."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ["exec", "admin"]
        )


class ShopItemViewSet(viewsets.ModelViewSet):
    """ViewSet for shop items."""

    queryset = ShopItem.objects.filter(available=True)
    serializer_class = ShopItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsExecOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for orders/claims."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Users see only their orders; execs see all."""
        if self.request.user.role in ["exec", "admin"]:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def claim_item(self, request):
        """Claim an item from the shop."""
        item_id = request.data.get("item_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            item = ShopItem.objects.get(id=item_id, available=True)
        except ShopItem.DoesNotExist:
            return Response(
                {"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user = request.user
        total_points = (
            user.point_transactions.aggregate(total=Sum("amount"))["total"] or 0
        )
        cost = item.cost * quantity

        if total_points < cost:
            return Response(
                {
                    "error": f"Insufficient points. You have {total_points}, need {cost}",
                    "points_available": total_points,
                    "cost": cost,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = Order.objects.create(
            user=user, item=item, quantity=quantity, status=Order.Status.PENDING
        )
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """Approve an order (exec only)."""
        if request.user.role not in ["exec", "admin"]:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        order = self.get_object()
        order.status = Order.Status.APPROVED
        order.approved_by = request.user
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def mark_claimed(self, request, pk=None):
        """Mark order as claimed (exec only)."""
        if request.user.role not in ["exec", "admin"]:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        order = self.get_object()
        if order.status != Order.Status.APPROVED:
            return Response(
                {"error": "Order must be approved first"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = Order.Status.CLAIMED
        order.save()

        # Deduct points from user
        total_cost = order.item.cost * order.quantity
        PointTransaction.objects.create(
            user=order.user,
            amount=-total_cost,
            reason=f"Claimed {order.quantity}x {order.item.name}",
            awarded_by=request.user,
        )

        serializer = self.get_serializer(order)
        return Response(serializer.data)


class PointTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing point transactions."""

    queryset = PointTransaction.objects.all()
    serializer_class = PointTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Users see only their transactions; execs see all."""
        if self.request.user.role in ["exec", "admin"]:
            return PointTransaction.objects.all()
        return PointTransaction.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def award_points(self, request):
        """Award points to a user (exec only)."""
        if request.user.role not in ["exec", "admin"]:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        user_id = request.data.get("user_id")
        amount = request.data.get("amount")
        reason = request.data.get("reason", "Points awarded")

        if not user_id or not amount:
            return Response(
                {"error": "user_id and amount required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        transaction = PointTransaction.objects.create(
            user=user, amount=amount, reason=reason, awarded_by=request.user
        )
        serializer = self.get_serializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def my_balance(self, request):
        """Get current user's point balance."""
        total = (
            request.user.point_transactions.aggregate(total=Sum("amount"))["total"] or 0
        )
        return Response({"points": total})
