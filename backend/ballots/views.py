"""Views for ballots app - voting system."""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from .models import Ballot, BallotOption, Vote
from .serializers import BallotSerializer, BallotOptionSerializer, VoteSerializer


class IsExecOrReadOnly(permissions.BasePermission):
    """Execs can create ballots, everyone can vote."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST" and view.basename == "vote-list":
            return request.user and request.user.is_authenticated
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ["exec", "admin"]
        )


class BallotViewSet(viewsets.ModelViewSet):
    """ViewSet for ballots."""

    queryset = Ballot.objects.all()
    serializer_class = BallotSerializer
    permission_classes = [permissions.IsAuthenticated, IsExecOrReadOnly]
    ordering_fields = ["created_at", "closing_date"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def add_option(self, request, pk=None):
        """Add an option to a ballot (exec only)."""
        if request.user.role not in ["exec", "admin"]:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        ballot = self.get_object()
        text = request.data.get("text")

        if not text:
            return Response(
                {"error": "text required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if ballot.closed:
            return Response(
                {"error": "Ballot is closed"}, status=status.HTTP_400_BAD_REQUEST
            )

        option = BallotOption.objects.create(ballot=ballot, text=text)
        serializer = BallotOptionSerializer(option)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def results(self, request, pk=None):
        """Get detailed results of a ballot."""
        ballot = self.get_object()
        results = []

        for option in ballot.options.all():
            vote_count = option.votes.count()
            results.append(
                {
                    "id": option.id,
                    "text": option.text,
                    "votes": vote_count,
                    "percentage": (
                        round((vote_count / ballot.votes.count() * 100), 2)
                        if ballot.votes.count() > 0
                        else 0
                    ),
                }
            )

        return Response(
            {
                "ballot_id": ballot.id,
                "title": ballot.title,
                "total_votes": ballot.votes.count(),
                "options": sorted(results, key=lambda x: x["votes"], reverse=True),
            }
        )

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def close(self, request, pk=None):
        """Close a ballot (exec only)."""
        if request.user.role not in ["exec", "admin"]:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        ballot = self.get_object()
        ballot.close_ballot()
        serializer = self.get_serializer(ballot)
        return Response(serializer.data)


class VoteViewSet(viewsets.ModelViewSet):
    """ViewSet for casting and managing votes."""

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def cast_vote(self, request):
        """Cast a vote on a ballot."""
        ballot_id = request.data.get("ballot_id")
        option_id = request.data.get("option_id")

        if not ballot_id or not option_id:
            return Response(
                {"error": "ballot_id and option_id required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ballot = Ballot.objects.get(id=ballot_id)
        except Ballot.DoesNotExist:
            return Response(
                {"error": "Ballot not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if ballot is open
        if ballot.closed or timezone.now() >= ballot.closing_date:
            return Response(
                {"error": "Ballot is closed"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if option belongs to this ballot
        try:
            option = BallotOption.objects.get(id=option_id, ballot=ballot)
        except BallotOption.DoesNotExist:
            return Response(
                {"error": "Option not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Create or update vote
        vote, created = Vote.objects.update_or_create(
            ballot=ballot, user=request.user, defaults={"option": option}
        )

        serializer = self.get_serializer(vote)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def my_votes(self, request):
        """Get current user's votes."""
        votes = Vote.objects.filter(user=request.user)
        serializer = self.get_serializer(votes, many=True)
        return Response(serializer.data)
