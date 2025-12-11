# 📂 RuseHAC Project Structure

```
RuseHAC/
│
├── 📄 README.md                    # Main project documentation (READ THIS FIRST!)
├── 📄 QUICKSTART.md                # 5-minute quick start guide
├── 📄 SCAFFOLD_SUMMARY.md          # What was scaffolded in Task 1
├── 📄 DJANGO_COMMANDS.md           # Django CLI commands reference
├── 📄 .env.example                 # Environment variables template
├── 📄 requirements.txt             # Python dependencies
├── 📄 package.json                 # Node.js dependencies
├── 📄 LICENSE                      # MIT License
├── 🔧 dev.sh                       # Quick backend startup script
├── 🔧 index.js                     # (legacy file - can remove)
├── 🔧 main.py                      # (legacy file - can remove)
├── 🔧 database_manager.py          # (legacy file - can remove)
│
├── 📦 backend/                     # Django REST API Server
│   │
│   ├── 🔧 manage.py                # Django management script
│   │
│   ├── ⚙️ config/                  # Django project configuration
│   │   ├── __init__.py
│   │   ├── settings.py             # ⭐ Main settings (apps, middleware, DB, email, etc)
│   │   ├── urls.py                 # ⭐ Main URL routing (maps to all apps)
│   │   ├── wsgi.py                 # WSGI server config (for production)
│   │   └── asgi.py                 # ASGI config (WebSockets)
│   │
│   ├── 👤 accounts/                # User authentication & profiles
│   │   ├── models.py               # ⭐ CustomUser, ExecApplication
│   │   ├── views.py                # ⭐ UserViewSet, ExecApplicationViewSet
│   │   ├── serializers.py          # User serialization for API
│   │   ├── urls.py                 # API routes (/api/accounts/*)
│   │   ├── admin.py                # Django admin configuration
│   │   ├── apps.py                 # App configuration
│   │   └── __init__.py
│   │
│   ├── 📢 core/                    # Announcements & attendance
│   │   ├── models.py               # ⭐ Announcement, Meeting, Attendance
│   │   ├── views.py                # ⭐ Announcement, Meeting, Attendance ViewSets
│   │   ├── serializers.py          # Serializers for API
│   │   ├── urls.py                 # API routes (/api/core/*)
│   │   ├── admin.py                # Django admin
│   │   ├── apps.py
│   │   └── __init__.py
│   │
│   ├── 🛍️ shop/                    # Points system & shop
│   │   ├── models.py               # ⭐ ShopItem, Order, PointTransaction
│   │   ├── views.py                # ⭐ Shop endpoints (award points, place orders)
│   │   ├── urls.py                 # API routes (/api/shop/*)
│   │   ├── admin.py                # Django admin
│   │   ├── apps.py
│   │   └── __init__.py
│   │
│   ├── 🗳️ ballots/                 # Voting system
│   │   ├── models.py               # ⭐ Ballot, BallotOption, Vote
│   │   ├── urls.py
│   │   ├── admin.py                # Django admin
│   │   ├── apps.py
│   │   └── __init__.py
│   │
│   ├── 📚 resources/               # Resource drive & submissions
│   │   ├── models.py               # ⭐ Resource, Submission, SubmissionFeedback
│   │   ├── urls.py
│   │   ├── admin.py                # Django admin
│   │   ├── apps.py
│   │   └── __init__.py
│   │
│   ├── 💬 chat/                    # Real-time messaging
│   │   ├── models.py               # ⭐ ChatRoom, ChatMessage
│   │   ├── consumers.py            # ⭐ WebSocket consumers (for real-time chat)
│   │   ├── urls.py
│   │   ├── admin.py                # Django admin
│   │   ├── apps.py
│   │   └── __init__.py
│   │
│   ├── 🔔 notifications/           # Notifications & email feed
│   │   ├── models.py               # ⭐ Notification model
│   │   ├── urls.py
│   │   ├── admin.py                # Django admin
│   │   ├── apps.py
│   │   └── __init__.py
│   │
│   ├── 📄 templates/               # (Optional) Server-rendered templates
│   ├── 🎨 static/                  # (Optional) Static files
│   ├── 🗂️ media/                   # User uploads (shop items, resources, submissions)
│   └── 💾 db.sqlite3               # Development database (SQLite)
│
├── 🎨 public/                      # Frontend (HTML/CSS/JS/React)
│   │
│   ├── 📄 index.html               # Main HTML file
│   ├── 📄 files.txt                # (legacy)
│   ├── 📄 folders.txt              # (legacy)
│   ├── 🔧 serviceWorker.js         # (legacy)
│   │
│   ├── 🎨 css/
│   │   └── style.css               # Main stylesheet
│   │
│   ├── 🎨 icons/                   # App icons
│   │
│   ├── 📸 images/                  # App images & assets
│   │
│   └── 📝 js/
│       └── app.js                  # React app entry point (TO BE BUILT)
│
└── 🔧 node_modules/                # Node dependencies (after npm install)
```

---

## 🎯 Key Files to Understand

### Backend (Django)

1. **`backend/config/settings.py`** ⭐⭐⭐
   - Configure apps, middleware, database, email, JWT, CORS
   - Add new installed apps here
   - Environment variables loaded here

2. **`backend/config/urls.py`** ⭐⭐
   - Main URL routing
   - Maps `/api/accounts/` to accounts app, etc.
   - Add new app routes here

3. **`backend/*/models.py`** ⭐⭐⭐
   - Database models (User, Announcement, Meeting, etc.)
   - Define relationships here
   - Run migrations after changes

4. **`backend/*/views.py`** ⭐⭐⭐
   - API endpoints and business logic
   - ViewSets handle GET/POST/PUT/DELETE
   - Add custom actions here

5. **`backend/*/serializers.py`** ⭐⭐
   - Convert models to/from JSON
   - Validation happens here
   - Define which fields to expose

6. **`backend/*/admin.py`** ⭐
   - Django admin UI configuration
   - Already set up for all models

### Frontend (React)

1. **`package.json`** ⭐
   - Node.js dependencies
   - npm scripts (start, build, test)

2. **`public/index.html`** ⭐
   - Main HTML file
   - React app mounts here

3. **`public/js/app.js`** ⭐⭐⭐
   - React components
   - API calls to backend
   - Page routing

4. **`public/css/style.css`** ⭐⭐
   - App styling
   - Responsive design
   - Theme customization

---

## 🔄 Request Flow

```
Browser → React (port 3000)
           ↓
           Axios API Call
           ↓
         Django (port 8000)
           ↓
           DRF ViewSet
           ↓
           Model
           ↓
         Database (SQLite/PostgreSQL)
           ↓
        Serializer
           ↓
          JSON Response
           ↓
         React Updates UI
```

---

## 📋 What Each App Does

| App | Purpose | Key Models | API Route |
|-----|---------|-----------|-----------|
| **accounts** | User auth & profiles | CustomUser, ExecApplication | `/api/accounts/` |
| **core** | Announcements & attendance | Announcement, Meeting, Attendance | `/api/core/` |
| **shop** | Points & merchandise | ShopItem, Order, PointTransaction | `/api/shop/` |
| **ballots** | Voting system | Ballot, Vote, BallotOption | `/api/ballots/` |
| **resources** | Resource drive | Resource, Submission, Feedback | `/api/resources/` |
| **chat** | Real-time messaging | ChatRoom, ChatMessage | `/api/chat/` + WebSocket |
| **notifications** | Email & feed | Notification | `/api/notifications/` |

---

## 🚀 First Steps After Scaffolding

1. **Read QUICKSTART.md** - Get the server running
2. **Create a superuser** - `python manage.py createsuperuser`
3. **Visit Django admin** - `http://localhost:8000/admin`
4. **Create test data** - Add announcements, meetings, etc. in admin
5. **Check API endpoints** - Visit `http://localhost:8000/api/accounts/users/`
6. **Build React components** - Connect frontend to backend APIs

---

## 💡 Important Notes

- **⭐** marks the most important files to understand
- **Color coding**: 🔧 (code), 📄 (docs), 🎨 (frontend), ⚙️ (config)
- Django admin at `/admin` is your friend for testing data
- Frontend proxies to backend via `package.json` proxy setting
- All static files (CSS, images) served from `/public`

---

## 🔜 Next: Build the API (Task 2)

Once you understand this structure, you're ready to:
1. Add serializers for all models
2. Implement viewset actions
3. Add authentication/permissions
4. Build React components
5. Test API endpoints

Good luck! 🚀
