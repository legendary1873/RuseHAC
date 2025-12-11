# 🎬 Getting Started - Run the Code

## Step 1: Install Dependencies

```bash
cd RuseHAC
pip install -r requirements.txt
```

If you get errors, you may need to install system dependencies for `psycopg2`:
```bash
# macOS
brew install postgresql

# Ubuntu
sudo apt-get install libpq-dev python3-dev

# Then retry pip install
```

## Step 2: Create Database

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

Expected output:
```
Applying accounts.0001_initial... OK
Applying core.0001_initial... OK
Applying shop.0001_initial... OK
Applying ballots.0001_initial... OK
...
```

## Step 3: Create Admin User

```bash
python manage.py createsuperuser
```

Enter:
- Email: `admin@example.com`
- Password: `AdminPass123!`

## Step 4: Create Sample Data (Optional)

```bash
python manage.py shell
```

Then paste:
```python
from accounts.models import CustomUser
from core.models import Announcement, Meeting
from shop.models import ShopItem
from ballots.models import Ballot, BallotOption
from django.utils import timezone
from datetime import timedelta

# Create test user
user = CustomUser.objects.create_user(
    email='member@example.com',
    first_name='John',
    last_name='Member',
    year_group='Y10',
    password='TestPass123!'
)

# Create test exec
exec_user = CustomUser.objects.create_user(
    email='exec@example.com',
    first_name='Jane',
    last_name='Exec',
    year_group='Y13',
    role='exec',
    password='TestPass123!'
)

# Award some points
from shop.models import PointTransaction
PointTransaction.objects.create(
    user=user,
    amount=150,
    reason='Attendance bonus',
    awarded_by=exec_user
)

# Create announcement
Announcement.objects.create(
    title='Welcome to RuseHAC!',
    content='This is a test announcement. Check back for club updates.',
    author=exec_user,
    pinned=True
)

# Create shop item
ShopItem.objects.create(
    name='History Club Sticker Pack',
    description='Pack of 5 exclusive history-themed stickers',
    cost=50,
    available=True
)

# Create meeting
meeting = Meeting.objects.create(
    title='Weekly Meeting',
    date=timezone.now() + timedelta(days=1),
    created_by=exec_user
)

# Create ballot
ballot = Ballot.objects.create(
    title='What should we study next?',
    description='Vote for the next historical period to explore',
    created_by=exec_user,
    closing_date=timezone.now() + timedelta(days=7)
)

# Add ballot options
BallotOption.objects.create(ballot=ballot, text='Victorian Era')
BallotOption.objects.create(ballot=ballot, text='Ancient Rome')
BallotOption.objects.create(ballot=ballot, text='Medieval Europe')

print("✅ Test data created!")
```

Type `exit()` to leave shell.

## Step 5: Start the Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Step 6: Verify Everything Works

### Access Django Admin
- Go to: http://localhost:8000/admin
- Login with admin credentials
- You should see all models (Announcements, Meetings, Ballots, etc.)

### Test API Endpoints

Open another terminal and test:

```bash
# Register
curl -X POST http://localhost:8000/api/accounts/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "year_group": "Y9",
    "password": "Password123!",
    "password2": "Password123!"
  }'

# Login
curl -X POST http://localhost:8000/api/accounts/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser@example.com",
    "password": "Password123!"
  }'

# Get current user (use access token from login response)
curl -X GET http://localhost:8000/api/accounts/users/me/ \
  -H "Authorization: Bearer <your_access_token>"

# Get announcements
curl http://localhost:8000/api/core/announcements/

# Get ballots
curl http://localhost:8000/api/ballots/ballots/

# Get shop items
curl http://localhost:8000/api/shop/items/
```

## Troubleshooting

### "module named django not found"
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or just activate venv
pip install -r requirements.txt
```

### "Database locked" (SQLite)
```bash
rm db.sqlite3
python manage.py migrate
```

### Port 8000 already in use
```bash
python manage.py runserver 8001  # Use different port
```

### Migrations not working
```bash
# Reset migrations (CAUTION: loses data)
python manage.py migrate accounts zero
python manage.py migrate core zero
# Then:
python manage.py migrate
```

## Next Steps

Once everything is running:

1. **Build React components** to consume the API
2. **Add the remaining features** (chat, resources, notifications)
3. **Write tests** for all endpoints
4. **Deploy** to production

See `FEATURES_IMPLEMENTED.md` for complete API documentation.

---

## 🎯 Common Commands

```bash
# Run tests
python manage.py test

# Create new admin user
python manage.py createsuperuser

# Access database shell
python manage.py dbshell

# Check for issues
python manage.py check

# View all database tables
python manage.py show_urls

# Dump data
python manage.py dumpdata > data.json

# Load data
python manage.py loaddata data.json
```

Good luck! 🚀
