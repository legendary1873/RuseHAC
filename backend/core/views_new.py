"""Views for core app - announcements, meetings, attendance."""

from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Announcement, Meeting, Attendance
from .serializers_new import (
    AnnouncementSerializer,
    MeetingSerializer,
    AttendanceSerializer,
    AttendanceStatsSerializer,
)


class IsExecOrReadOnly(permissions.BasePermission):
    """Permission: Execs can edit/create, others read-only."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ["exec", "admin"]
        )


class AnnouncementViewSet(viewsets.ModelViewSet):
    """ViewSet for announcements."""

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated, IsExecOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "pinned"]
    ordering = ["-pinned", "-created_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def pin(self, request, pk=None):
        """Pin/unpin announcement (exec only)."""
        if request.user.role not in ["exec", "admin"]:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        announcement = self.get_object()
        announcement.pinned = not announcement.pinned
        announcement.save()
        serializer = self.get_serializer(announcement)
        return Response(serializer.data)


class MeetingViewSet(viewsets.ModelViewSet):
    """ViewSet for meetings."""

    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated, IsExecOrReadOnly]
    ordering_fields = ["date"]
    ordering = ["-date"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def mark_attendance(self, request, pk=None):
        """Mark users as attending a meeting (exec only)."""
        if request.user.role not in ["exec", "admin"]:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        meeting = self.get_object()
        user_ids = request.data.get("user_ids", [])

        if not user_ids:
            return Response(
                {"error": "user_ids required"}, status=status.HTTP_400_BAD_REQUEST
            )

        from django.contrib.auth import get_user_model

        User = get_user_model()

        created_count = 0
        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id, is_active=True)
                _, created = Attendance.objects.get_or_create(
                    user=user, meeting=meeting, defaults={"marked_by": request.user}
                )
                if created:
                    created_count += 1
            except User.DoesNotExist:
                pass

        return Response(
            {"created": created_count, "attendance_count": meeting.attendances.count()},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["get"])
    def attendance_list(self, request, pk=None):
        """Get attendance list for a meeting."""
        meeting = self.get_object()
        attendances = meeting.attendances.all()
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)


class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing attendance records."""

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def my_stats(self, request):
        """Get current user's attendance stats."""
        user = request.user
        today = timezone.now()

        # Calculate from start of current academic term (September)
        current_year = today.year
        if today.month < 9:
            term_start = today.replace(year=current_year - 1, month=9, day=1)
        else:
            term_start = today.replace(month=9, day=1)

        total_meetings = Meeting.objects.filter(date__gte=term_start).count()
        attended = Attendance.objects.filter(
            user=user, meeting__date__gte=term_start
        ).count()

        if total_meetings == 0:
            percentage = 0
            remaining_needed = 0
        else:
            percentage = round((attended / total_meetings * 100), 2)
            # Calculate how many more meetings needed to reach 70%
            target = int(total_meetings * 0.7)
            remaining_needed = max(0, target - attended)

        data = {
            "attended": attended,
            "total": total_meetings,
            "percentage": percentage,
            "target_percentage": 70,
            "on_target": percentage >= 70,
            "remaining_needed": remaining_needed,
        }

        serializer = AttendanceStatsSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def leaderboard(self, request):
        """Get attendance leaderboard (top attendees)."""
        from django.db.models import Count, Q
        from django.contrib.auth import get_user_model

        User = get_user_model()
        today = timezone.now()

        current_year = today.year
        if today.month < 9:
            term_start = today.replace(year=current_year - 1, month=9, day=1)
        else:
            term_start = today.replace(month=9, day=1)

        total_meetings = Meeting.objects.filter(date__gte=term_start).count()

        if total_meetings == 0:
            return Response([])

        # Get users with attendance count
        users = (
            User.objects.filter(is_active=True, is_banned=False)
            .annotate(
                attended_count=Count(
                    "attendance_records",
                    filter=Q(attendance_records__meeting__date__gte=term_start),
                )
            )
            .order_by("-attended_count")[:20]
        )

        leaderboard_data = [
            {
                "id": user.id,
                "email": user.email,
                "name": f"{user.first_name} {user.last_name}".strip(),
                "attended": user.attended_count,
                "total": total_meetings,
                "percentage": round((user.attended_count / total_meetings * 100), 2),
            }
            for user in users
        ]

        return Response(leaderboard_data)
