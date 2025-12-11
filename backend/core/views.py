"""Views for core app."""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from datetime import timedelta
from .models import Announcement, Meeting, Attendance
from .serializers import AnnouncementSerializer, MeetingSerializer, AttendanceSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    """ViewSet for announcements."""

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "pinned"]
    ordering = ["-pinned", "-created_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ["create", "update", "destroy", "partial_update"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class MeetingViewSet(viewsets.ModelViewSet):
    """ViewSet for meetings."""

    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser()])
    def take_attendance(self, request, pk=None):
        """Mark users as attending a meeting."""
        meeting = self.get_object()
        user_ids = request.data.get("user_ids", [])
        created_count = 0
        for user_id in user_ids:
            _, created = Attendance.objects.get_or_create(
                user_id=user_id, meeting=meeting, defaults={"marked_by": request.user}
            )
            if created:
                created_count += 1
        return Response({"created": created_count}, status=status.HTTP_201_CREATED)


class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing attendance records."""

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def my_attendance(self, request):
        """Get current user's attendance and calculate percentage."""
        user = request.user
        today = timezone.now()
        term_start = today.replace(month=9, day=1)  # Start of academic term

        total_meetings = Meeting.objects.filter(date__gte=term_start).count()
        attended = Attendance.objects.filter(
            user=user, meeting__date__gte=term_start
        ).count()
        percentage = (attended / total_meetings * 100) if total_meetings > 0 else 0

        return Response(
            {
                "attended": attended,
                "total": total_meetings,
                "percentage": round(percentage, 2),
                "target_percentage": 70,
                "on_target": percentage >= 70,
            }
        )
