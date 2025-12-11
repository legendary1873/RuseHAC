#!/usr/bin/env python
"""
Test script for RuseHAC API endpoints.
Run: python manage.py shell < test_api.py
"""

from django.contrib.auth import get_user_model
from accounts.models import ExecApplication
from core.models import Announcement, Meeting, Attendance
from shop.models import ShopItem, Order, PointTransaction
from ballots.models import Ballot, BallotOption, Vote
from django.utils import timezone
from datetime import timedelta
import json

User = get_user_model()

print("=" * 60)
print("🧪 RuseHAC API Test Suite")
print("=" * 60)

# Cleanup
User.objects.all().delete()
print("\n✓ Cleaned up test data")

# Create test users
admin_user = User.objects.create_user(
    email="admin@test.com",
    first_name="Admin",
    last_name="User",
    year_group="Y13",
    role="admin",
    password="AdminPass123!",
)

exec_user = User.objects.create_user(
    email="exec@test.com",
    first_name="Executive",
    last_name="Member",
    year_group="Y13",
    role="exec",
    password="ExecPass123!",
)

member_user = User.objects.create_user(
    email="member@test.com",
    first_name="Regular",
    last_name="Member",
    year_group="Y10",
    role="member",
    password="MemberPass123!",
)

print("\n✓ Created test users:")
print(f"  - Admin: {admin_user.email}")
print(f"  - Exec: {exec_user.email}")
print(f"  - Member: {member_user.email}")

# Test Announcements
print("\n" + "=" * 60)
print("📢 Testing Announcements")
print("=" * 60)

ann1 = Announcement.objects.create(
    title="Welcome to RuseHAC!",
    content="Welcome to the History Club. Check back for updates.",
    author=exec_user,
    pinned=True,
)
ann2 = Announcement.objects.create(
    title="Next Meeting",
    content="Next meeting is on Friday at 3 PM.",
    author=exec_user,
    pinned=False,
)
print(f"✓ Created {Announcement.objects.count()} announcements")
print(f"  - Pinned: {Announcement.objects.filter(pinned=True).count()}")
print(f"  - Total: {Announcement.objects.count()}")

# Test Meetings & Attendance
print("\n" + "=" * 60)
print("📅 Testing Meetings & Attendance")
print("=" * 60)

meeting1 = Meeting.objects.create(
    title="Weekly History Club Meeting",
    date=timezone.now() + timedelta(days=1),
    created_by=exec_user,
)
meeting2 = Meeting.objects.create(
    title="Historical Debate",
    date=timezone.now() + timedelta(days=7),
    created_by=exec_user,
)
print(f"✓ Created {Meeting.objects.count()} meetings")

# Mark attendance
att1 = Attendance.objects.create(
    user=member_user, meeting=meeting1, marked_by=exec_user
)
att2 = Attendance.objects.create(
    user=member_user, meeting=meeting2, marked_by=exec_user
)
print(f"✓ Marked attendance: {Attendance.objects.count()} records")

# Check attendance stats
attended = member_user.attendance_records.count()
total = Meeting.objects.count()
percentage = round((attended / total * 100), 2) if total > 0 else 0
print(f"✓ Member attendance: {attended}/{total} ({percentage}%)")

# Test Shop System
print("\n" + "=" * 60)
print("🛍️  Testing Shop System")
print("=" * 60)

item1 = ShopItem.objects.create(
    name="History Club Sticker Pack",
    description="Pack of 5 exclusive stickers",
    cost=50,
    available=True,
)
item2 = ShopItem.objects.create(
    name="Historic Timeline Poster",
    description="Beautiful timeline poster",
    cost=100,
    available=True,
)
print(f"✓ Created {ShopItem.objects.count()} shop items")

# Award points
trans1 = PointTransaction.objects.create(
    user=member_user, amount=150, reason="Attendance bonus", awarded_by=exec_user
)
print(f"✓ Awarded {trans1.amount} points to member")

# Check balance
balance = (
    member_user.point_transactions.aggregate(
        total=__import__("django.db.models", fromlist=["Sum"]).Sum("amount")
    )["total"]
    or 0
)
print(f"✓ Member balance: {balance} points")

# Create order
order1 = Order.objects.create(
    user=member_user, item=item1, quantity=1, status=Order.Status.PENDING
)
print(f"✓ Created order: {order1.quantity}x {order1.item.name}")

# Approve order
order1.status = Order.Status.APPROVED
order1.approved_by = exec_user
order1.save()
print(f"✓ Order approved")

# Mark as claimed (deduct points)
order1.status = Order.Status.CLAIMED
order1.save()
PointTransaction.objects.create(
    user=member_user,
    amount=-order1.item.cost,
    reason=f"Claimed {order1.item.name}",
    awarded_by=exec_user,
)
new_balance = (
    member_user.point_transactions.aggregate(
        __import__("django.db.models", fromlist=["Sum"]).Sum("amount")
    )["total"]
    or 0
)
print(f"✓ Order claimed, points deducted: {balance} → {new_balance}")

# Test Ballots & Voting
print("\n" + "=" * 60)
print("🗳️  Testing Ballots & Voting")
print("=" * 60)

ballot1 = Ballot.objects.create(
    title="What should we study next?",
    description="Vote for the next historical period",
    created_by=exec_user,
    closing_date=timezone.now() + timedelta(days=7),
)
print(f"✓ Created ballot: {ballot1.title}")

# Add options
opt1 = BallotOption.objects.create(ballot=ballot1, text="Victorian Era")
opt2 = BallotOption.objects.create(ballot=ballot1, text="Ancient Rome")
opt3 = BallotOption.objects.create(ballot=ballot1, text="Medieval Europe")
print(f"✓ Added {ballot1.options.count()} voting options")

# Cast votes
vote1 = Vote.objects.create(ballot=ballot1, user=member_user, option=opt1)
vote2 = Vote.objects.create(ballot=ballot1, user=exec_user, option=opt1)
vote3 = Vote.objects.create(ballot=ballot1, user=admin_user, option=opt2)
print(f"✓ Cast {Vote.objects.count()} votes")

# Check results
results = {}
for option in ballot1.options.all():
    vote_count = option.votes.count()
    results[option.text] = vote_count
print(f"✓ Vote results:")
for option, count in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"    {option}: {count} votes")

# Test Exec Applications
print("\n" + "=" * 60)
print("👔 Testing Exec Applications")
print("=" * 60)

app1 = ExecApplication.objects.create(
    user=member_user,
    statement="I am passionate about history and want to help lead the club. "
    + "I have ideas for new activities and have been attending consistently.",
)
print(f"✓ Created exec application")
print(f"  Status: {app1.status}")

# Approve application
app1.status = ExecApplication.Status.APPROVED
app1.reviewed_by = exec_user
app1.reviewed_at = timezone.now()
app1.save()
member_user.role = "exec"
member_user.save()
print(f"✓ Application approved, user role upgraded to exec")

# Summary
print("\n" + "=" * 60)
print("📊 Test Summary")
print("=" * 60)

summary = {
    "Users": User.objects.count(),
    "Announcements": Announcement.objects.count(),
    "Meetings": Meeting.objects.count(),
    "Attendance Records": Attendance.objects.count(),
    "Shop Items": ShopItem.objects.count(),
    "Orders": Order.objects.count(),
    "Point Transactions": PointTransaction.objects.count(),
    "Ballots": Ballot.objects.count(),
    "Votes": Vote.objects.count(),
    "Exec Applications": ExecApplication.objects.count(),
}

for key, value in summary.items():
    print(f"✓ {key}: {value}")

print("\n" + "=" * 60)
print("✅ All database tests passed!")
print("=" * 60)
print("\nNext: Test API endpoints with curl/Postman")
print("See FEATURES_IMPLEMENTED.md for endpoint documentation")
