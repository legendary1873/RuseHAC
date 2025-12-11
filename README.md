# RuseHAC - JRAHS History Appreciation Club Website

A comprehensive web platform for Ruse History Appreciation Club.

**Author:** Jiayu Hu (<jiayu.hu1@education.nsw.gov.au>)

---

## Features

### For All Members
- **User Accounts**: Sign up with email, name, and year group. Email-based gravatar profile pictures.
- **Profiles**: View and customize your profile with bio and year group. Search and view other members' profiles.
- **Announcements**: Stay updated with pinned announcements from execs.
- **Voting**: Participate in ballots for new topics, exec positions, and club activities.
- **Points & Shop**: Earn points from attendance and special activities. Claim stickers and other merch from the shop.
- **Resource Drive**: Access shared notes, class materials, textbooks, past papers, and exam questions.
- **Submissions**: Submit history essays for feedback from execs and peers.
- **Group Chat**: Real-time messaging in the main club chat (Discord-like experience).
- **Attendance Tracker**: View your term attendance percentage and track progress toward 70% attendance goal.
- **Notifications**: In-app feed + email notifications (customizable in settings).
- **Settings**: Customize notifications and other preferences.

### For Execs
- **All member features**, as well as:
- **Create Announcements**: Post important updates and pin them.
- **Create Ballots**: Set up voting for topics, exec positions, and activities with custom closing dates.
- **Manage Attendance**: Mark members as present at meetings and view attendance analytics.
- **Award Points**: Give members points for participation and achievements.
- **Moderation**: Temporarily ban members for misuse; manage user behavior.
- **Admin Chat**: Private exec-only chat for planning and discussions.
- **Manage Resources**: Approve user submissions to the resource drive.
- **Manage Members**: View all members, roles, and applications.

### For Admins
- Full control over settings, roles, and site configuration.
- Django admin panel for database management.

---

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Frontend**: React (served from `/public/js/`)
- **Database**: PostgreSQL (or SQLite for development)
- **Real-time**: Django Channels + WebSockets
- **Task Queue**: Celery + Redis (for email notifications)
- **Authentication**: JWT + Session-based auth
- **Email**: SMTP (Gmail, SendGrid, etc.)

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL (or SQLite for dev)
- Node.js 16+ (for frontend)
- Redis (for Celery and WebSockets, optional for dev)

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/legendary1873/RuseHAC.git
   cd RuseHAC
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations:**
   ```bash
   cd backend
   python manage.py migrate
   ```

6. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   The backend will be available at `http://localhost:8000`

8. **Access the admin panel:**
   Navigate to `http://localhost:8000/admin` and log in with your superuser credentials.

### Frontend Setup

1. **Install Node dependencies:**
   ```bash
   npm install
   ```

2. **Run the development server:**
   ```bash
   npm start
   ```
   The frontend will be available at `http://localhost:3000`

3. **Build for production:**
   ```bash
   npm run build
   ```

---

## Project Structure

```
RuseHAC/
├── backend/                    # Django backend
│   ├── manage.py
│   ├── config/                # Django config
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── accounts/              # User auth & profiles
│   ├── core/                  # Announcements & attendance
│   ├── shop/                  # Points & shop system
│   ├── ballots/               # Voting system
│   ├── resources/             # Resource drive & submissions
│   ├── chat/                  # Group & private chat
│   ├── notifications/         # Notifications & email
│   └── db.sqlite3             # Dev database
├── public/                     # Static frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── css/
│   └── js/
│       └── app.js
├── requirements.txt           # Python dependencies
├── package.json              # Node.js dependencies
├── .env.example              # Environment template
├── LICENSE
└── README.md                 # This file
```

---

## API Endpoints

### Authentication
- `POST /api/accounts/users/register/` - Register new user
- `POST /api/accounts/users/login/` - Login
- `GET /api/accounts/users/me/` - Current user profile
- `POST /api/accounts/users/logout/` - Logout

### Users & Profiles
- `GET /api/accounts/users/` - List all users
- `GET /api/accounts/users/{id}/profile/` - Get user profile
- `PUT /api/accounts/users/{id}/` - Update profile
- `DELETE /api/accounts/users/delete_account/` - Delete account

### Announcements
- `GET /api/core/announcements/` - List announcements
- `POST /api/core/announcements/` - Create (exec only)
- `PUT /api/core/announcements/{id}/` - Update (exec only)

### Meetings & Attendance
- `GET /api/core/meetings/` - List meetings
- `POST /api/core/meetings/` - Create meeting (exec only)
- `POST /api/core/meetings/{id}/take_attendance/` - Mark attendance (exec only)
- `GET /api/core/attendance/my_attendance/` - Get your attendance stats

### Shop
- `GET /api/shop/items/` - List shop items
- `POST /api/shop/orders/` - Create order/claim
- `POST /api/shop/orders/award_points/` - Award points (exec only)

### Ballots
- `GET /api/ballots/` - List ballots
- `POST /api/ballots/` - Create ballot (exec only)
- `POST /api/ballots/{id}/vote/` - Cast a vote

### Resources
- `GET /api/resources/` - List resources
- `POST /api/resources/` - Upload resource
- `GET /api/resources/submissions/` - List submissions
- `POST /api/resources/submissions/` - Submit essay/draft

### Chat (WebSocket)
- `ws://localhost:8000/ws/chat/main/` - Main chat room
- `ws://localhost:8000/ws/chat/exec/` - Exec-only chat
- `ws://localhost:8000/ws/notifications/{user_id}/` - User notifications

### Notifications
- `GET /api/notifications/` - List notifications
- `PATCH /api/notifications/{id}/` - Mark as read
- `POST /api/notifications/unsubscribe/` - Unsubscribe from email

---

## User Roles & Permissions

| Feature | Member | Exec | Admin |
|---------|--------|------|-------|
| Create account | ✅ | ✅ | ✅ |
| View profiles | ✅ | ✅ | ✅ |
| Vote | ✅ | ✅ | ✅ |
| Apply for exec | ✅ | ❌ | ❌ |
| Create announcements | ❌ | ✅ | ✅ |
| Take attendance | ❌ | ✅ | ✅ |
| Award points | ❌ | ✅ | ✅ |
| Create ballots | ❌ | ✅ | ✅ |
| Manage resources | ❌ | ✅ | ✅ |
| Ban users | ❌ | ✅ | ✅ |
| Admin panel | ❌ | ❌ | ✅ |

---

## Deployment

### Using Heroku
```bash
heroku login
heroku create rusehac
git push heroku main
heroku run python backend/manage.py migrate
heroku run python backend/manage.py createsuperuser
```

### Using DigitalOcean / AWS
See `docs/deployment.md` for detailed instructions.

---

## Database Schema (Key Models)

### CustomUser
```python
- id, email (unique), username
- first_name, last_name
- year_group (Y7-Y13)
- role (member, exec, admin)
- bio, email_notifications
- is_banned, ban_reason, ban_until
```

### Announcement, Meeting, Attendance
```python
Announcement: title, content, author, pinned, created_at
Meeting: title, date, created_by
Attendance: user, meeting, marked_at, marked_by
```

### ShopItem, Order, PointTransaction
```python
ShopItem: name, description, cost (points), image
Order: user, item, quantity, status
PointTransaction: user, amount, reason, awarded_by
```

### Ballot, Vote, BallotOption
```python
Ballot: title, description, closing_date, created_by
BallotOption: ballot, text, vote_count
Vote: ballot, option, user (one per ballot)
```

### Resource, Submission, SubmissionFeedback
```python
Resource: title, file, category, tags, uploaded_by, approved
Submission: user, title, content, file
SubmissionFeedback: submission, given_by, feedback
```

---

## Testing

Run unit and integration tests:
```bash
cd backend
python manage.py test
```

Run with coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## Troubleshooting

**Issue: `ModuleNotFoundError: No module named 'django'`**
- Solution: Activate your virtual environment and run `pip install -r requirements.txt`

**Issue: `psycopg2` installation fails**
- Solution: Install PostgreSQL dev files or use SQLite in `.env` for development

**Issue: WebSocket connection fails**
- Solution: Ensure Redis is running and Channels is installed. Run: `redis-server` in another terminal

**Issue: Email not sending**
- Solution: Check `.env` email settings; use console backend for development

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/awesome-feature`
3. Commit changes: `git commit -m 'Add awesome feature'`
4. Push to branch: `git push origin feature/awesome-feature`
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the author.