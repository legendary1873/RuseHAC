# 🚀 Quick Start Guide - RuseHAC

## First-Time Setup (5 minutes)

### 1. Backend Setup
```bash
# Navigate to project
cd RuseHAC

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env

# Run migrations
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
