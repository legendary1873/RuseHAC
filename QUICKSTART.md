# RuseHAC - Quick Start Guide

This guide gets you from zero to a running RuseHAC platform in 10 minutes.

## 🚀 Super Quick Start (5 minutes)

### Prerequisites
- Python 3.9+ and pip
- Node.js 14+ and npm
- Git

### 1. Setup Backend (Terminal 1)

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create database
python manage.py migrate

# Create test data
python manage.py shell < test_api.py

# Run server
python manage.py runserver
# → API running at http://localhost:8000/api
```

### 2. Setup Frontend (Terminal 2)

```bash
# From project root /Users/jiayu/RuseHAC
npm install

# Start frontend server
npm run dev
# → Frontend running at http://localhost:3000
```

### 3. Login and Test

Open browser to **http://localhost:3000**

Test credentials:
- **Email**: `member@example.com`
- **Password**: `member123`

Expected: Dashboard with attendance stats, announcements, and user profile

---

## 📋 Detailed Setup Instructions

### Backend Setup (Detailed)

#### Step 1: Navigate to Backend
```bash
cd /Users/jiayu/RuseHAC/backend
```

#### Step 2: Create Python Virtual Environment
```bash
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
# On macOS: source venv/bin/activate
```

#### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

Packages installed:
- Django 4.2
- djangorestframework 3.14
- djangorestframework-simplejwt
- django-cors-headers
- django-channels 4.0
- celery 5.3
- redis 5.0
- psycopg2 (PostgreSQL driver)

#### Step 4: Run Migrations
```bash
python manage.py migrate
```

This creates all database tables.

#### Step 5: Create Test Data
```bash
python manage.py shell < test_api.py
```

This creates:
- 3 test users (admin, exec, member)
- 2 announcements (1 pinned)
- 3 meetings with attendance
- 5 shop items with orders
- 2 ballots with votes
- 1 exec application

#### Step 6: Run Django Development Server
```bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
```

**Backend is now running!** ✅

### Frontend Setup (Detailed)

#### Step 1: Navigate to Frontend Root
```bash
cd /Users/jiayu/RuseHAC
```

#### Step 2: Install Node Dependencies
```bash
npm install
```

Packages installed:
- express 4.18
- cors 2.8
- compression 1.7
- http-proxy-middleware 2.0
- dotenv 16.0

#### Step 3: Start Frontend Server
```bash
npm run dev
```

Expected output:
```
╔══════════════════════════════════════╗
║       RuseHAC Frontend Server        ║
╚══════════════════════════════════════╝

🚀 Server running at http://localhost:3000
📡 API proxied to http://localhost:8000
🔧 Environment: development
```

**Frontend is now running!** ✅

---

## 🎯 What to Test

### 1. Dashboard
1. Open http://localhost:3000
2. Click "Login"
3. Email: `member@example.com`
4. Password: `member123`
5. Click "Login"

**Expected**: 
- ✅ Dashboard loads
- ✅ Shows "Welcome, Member User!"
- ✅ Shows role, year group, points
- ✅ Shows attendance: 1/3 meetings (33%)
- ✅ Shows 70% target and "Need 2 more"
- ✅ Shows latest announcements

### 2. Voting
1. Click "Voting" in navbar
2. See 2 ballots
3. Click a vote button (e.g., "Yes")

**Expected**:
- ✅ Vote counts update
- ✅ Button turns green
- ✅ Can change vote

### 3. Shop
1. Click "Shop" in navbar
2. See items grid
3. Try to claim a 2-point item

**Expected**:
- ✅ Items displayed with point costs
- ✅ Current points shown
- ✅ Can claim affordable items
- ✅ See "Item claimed! Awaiting approval"

### 4. Logout
1. Click "Logout" in top right

**Expected**:
- ✅ Redirects to login page
- ✅ Can login again

---

## 🔧 Troubleshooting

### Backend Won't Start

**Error**: `ImportError: No module named 'django'`
```bash
# Solution: Ensure venv is activated and install requirements
source venv/bin/activate
pip install -r requirements.txt
```

**Error**: Port 8000 already in use
```bash
# Solution: Run on different port
python manage.py runserver 8001
# Then set API_URL=http://localhost:8001 for frontend
```

### Frontend Won't Start

**Error**: `npm: command not found`
```bash
# Solution: Install Node.js from https://nodejs.org/
```

**Error**: Port 3000 already in use
```bash
# Solution: Use different port
PORT=3001 npm run dev
# Open http://localhost:3001
```

### API Requests Fail

**Error in browser**: "Failed to connect to backend"
```bash
# Solution: Ensure backend is running
# Terminal 1: python manage.py runserver
# Terminal 2: npm run dev

# Check backend is accessible:
curl http://localhost:8000/api/accounts/token/
```

### Login Doesn't Work

**Error**: "Login failed" or 401
```bash
# Solution: Ensure test data was created
cd backend
python manage.py shell < test_api.py

# Try default credentials again:
# Email: member@example.com
# Password: member123
```

---

## 📊 Architecture Overview

```
User Browser (http://localhost:3000)
    ↓
Express.js Server (Node.js)
    ↓
Django REST API (http://localhost:8000/api)
    ↓
SQLite Database (database.db)
```

### Request Flow Example: Voting

1. User clicks vote button in React app
2. React sends POST request to `/api/ballots/votes/cast_vote/`
3. Express server proxies to Django backend
4. Django validates, creates Vote record
5. Django returns updated vote count
6. React updates UI with new count

---

## 🎓 Learning Resources

### Backend (Django)
- View code: `/Users/jiayu/RuseHAC/backend/accounts/views_new.py`
- Models: `/Users/jiayu/RuseHAC/backend/accounts/models.py`
- Serializers: `/Users/jiayu/RuseHAC/backend/accounts/serializers_new.py`
- API Endpoints: See `FEATURES_IMPLEMENTED.md`

### Frontend (React)
- Main app: `/Users/jiayu/RuseHAC/public/js/app_v2.jsx`
- Chat: `/Users/jiayu/RuseHAC/public/js/chat.jsx`
- Styles: `/Users/jiayu/RuseHAC/public/css/app.css`
- API Client: `/Users/jiayu/RuseHAC/public/js/api-client.js`

### Documentation
- Full API: `backend/FEATURES_IMPLEMENTED.md`
- Frontend Details: `FRONTEND_IMPLEMENTATION.md`
- Testing Guide: `FRONTEND_TESTING.md`
- Setup Guide: `FRONTEND_SETUP.md`

---

## 🚢 Deployment

### Simple Deployment (One Machine)

```bash
# Install production Node dependencies
npm install --production

# Run with PM2 (auto-restart on crash)
npm install -g pm2
pm2 start index.js --name rusehac-frontend

# Increase PM2 instances for load balancing
pm2 start index.js --name rusehac-frontend -i 4
```

### Docker Deployment

```bash
# Build frontend image
docker build -t rusehac-frontend .

# Run container
docker run -p 3000:3000 \
  -e API_URL=http://localhost:8000 \
  -e NODE_ENV=production \
  rusehac-frontend
```

### Production Checklist

- [ ] Set `API_URL` to production backend
- [ ] Set `NODE_ENV=production`
- [ ] Enable HTTPS (use reverse proxy like Nginx)
- [ ] Setup database backups
- [ ] Configure email for notifications
- [ ] Setup error logging
- [ ] Monitor performance

---

## 🤔 Common Questions

**Q: Can I run frontend and backend on the same machine?**
A: Yes! Default setup does this. Port 3000 (frontend) and 8000 (backend).

**Q: Can I deploy frontend and backend separately?**
A: Yes! Set `API_URL` environment variable to production backend URL.

**Q: Do I need PostgreSQL or can I use SQLite?**
A: SQLite works for development. For production, use PostgreSQL.

**Q: Can I use this on Windows?**
A: Yes! Use `venv\Scripts\activate` instead of `source venv/bin/activate`.

**Q: Can I modify the styles?**
A: Yes! Edit `/Users/jiayu/RuseHAC/public/css/app.css`.

**Q: Can I add new React components?**
A: Yes! Add to `public/js/` and import in `app_v2.jsx`.

---

## 📞 Need Help?

1. Check this guide first
2. Check `FRONTEND_TESTING.md` for testing help
3. Check `FRONTEND_SETUP.md` for setup issues
4. Check Django server logs for backend errors
5. Check browser console (F12) for frontend errors

---

## ✅ Success Checklist

- [ ] Backend running at http://localhost:8000
- [ ] Frontend running at http://localhost:3000
- [ ] Can login with member@example.com / member123
- [ ] Dashboard displays attendance stats
- [ ] Can vote on ballots
- [ ] Can claim shop items
- [ ] No errors in browser console (F12)
- [ ] No errors in terminal

**All checked? Congratulations! 🎉 RuseHAC is running!**

---

## 🔗 Next Steps

1. **Customize**: Edit styles, add your logo
2. **Populate**: Add real users and data
3. **Deploy**: Follow deployment section above
4. **Extend**: Add more features (see TODO in code)

---

**Version**: 1.0.0
**Last Updated**: 2024
**Status**: ✅ Ready to Run
cd backend
python manage.py migrate

# Create admin user (you'll set password interactively)
python manage.py createsuperuser

# Start backend server
python manage.py runserver
```
Backend runs at: **http://localhost:8000**
Admin panel: **http://localhost:8000/admin**

### 2. Frontend Setup
```bash
# In a NEW terminal window (keep backend running)
npm install
npm start
```
Frontend runs at: **http://localhost:3000**

---

## ✅ Verify Everything Works

1. Open **http://localhost:8000/admin** in browser
   - Log in with admin credentials you just created
   - You should see Django admin interface

2. Open **http://localhost:3000** in another tab
   - You should see the RuseHAC homepage (currently a placeholder)

3. In Django admin, try creating a test announcement:
   - Click "Announcements" → "Add Announcement"
   - Title: "Welcome to RuseHAC"
   - Content: "Club is live!"
   - Click Save

---

## 📝 Next Steps

- [ ] Read the full `README.md` to understand features
- [ ] Explore the Django models in `backend/accounts/models.py`
- [ ] Check out API endpoints documentation in README
- [ ] Start building React components in `public/js/`
- [ ] Run `python manage.py createsuperuser` to add more test users

---

## 🆘 Common Issues

### ❌ "django not found"
```bash
# Make sure venv is activated
source venv/bin/activate
# Then install again
pip install -r requirements.txt
```

### ❌ "npm: command not found"
- Install Node.js from https://nodejs.org/

### ❌ "port 8000 already in use"
```bash
# Kill the existing process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python manage.py runserver 8001
```

### ❌ Database locked (SQLite issue)
```bash
# Delete the database and recreate it
rm db.sqlite3
python manage.py migrate
```

---

## 🎯 Architecture Overview

```
Frontend (React)               Backend (Django)
   http://3000       ←→         http://8000
   /public/js/app.js            /api/...
   Components                   REST Endpoints
   State mgmt                    Authentication
                                 Database
```

---

## 💡 Key Commands

```bash
# Run migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Create Django superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Create a new app
python manage.py startapp app_name

# Access Django shell
python manage.py shell

# Run tests
python manage.py test

# Clear database (WARNING: destructive)
python manage.py flush
```

---

## 📚 File Structure You'll Edit

```
RuseHAC/
├── backend/
│   ├── accounts/models.py       ← User model (add fields here)
│   ├── core/views.py            ← Announcements, attendance logic
│   ├── shop/models.py           ← Shop items, points system
│   └── config/settings.py       ← App configuration
├── public/
│   ├── js/app.js                ← React components (build here!)
│   └── css/style.css            ← Styling
└── README.md                     ← Full documentation
```

---

## 🚢 Ready to Code?

Start with **Task 2: Design data models and API contract** from the main README.
Good luck! 🎉
