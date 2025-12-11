# 🛠️ Django Commands Reference

Quick reference for common Django commands used in RuseHAC development.

## 🚀 Server & Setup

```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8001

# Create database tables (after model changes)
python manage.py migrate

# Create initial migrations for a new app
python manage.py makemigrations app_name

# Create new Django app
python manage.py startapp new_app_name

# Create superuser (admin account)
python manage.py createsuperuser

# Interactive Python shell with Django context
python manage.py shell
```

## 🗄️ Database

```bash
# Apply all pending migrations
python manage.py migrate

# Show migrations for an app
python manage.py showmigrations accounts

# Migrate to specific migration
python manage.py migrate accounts 0003

# Undo all migrations for an app
python manage.py migrate accounts zero

# Create SQL for migrations without running them
python manage.py sqlmigrate accounts 0001

# Delete all data and reset database (WARNING: destructive)
python manage.py flush

# Show all database tables
python manage.py dbshell
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test accounts

# Run specific test class
python manage.py test accounts.tests.UserTestCase

# Run with verbose output
python manage.py test --verbosity=2

# Keep test database after running
python manage.py test --keepdb
```

## 📊 Admin & Data

```bash
# Open admin site at /admin
# Create objects in Django admin

# Load initial data from fixtures
python manage.py loaddata initial_data

# Export data to JSON
python manage.py dumpdata accounts > accounts_data.json

# Create sample data
python manage.py shell
# Then in shell:
# from accounts.models import CustomUser
# CustomUser.objects.create_user(email='test@example.com', password='pass123', year_group='Y10')
```

## 🔍 Debugging

```bash
# Run with debugging server (better error messages)
python manage.py runserver --pdb-on-error

# Check for common issues
python manage.py check

# List all installed apps and models
python manage.py show_urls

# Inspect a model
python manage.py inspectdb table_name
```

## 📦 Dependencies

```bash
# List installed packages
pip list

# Check for outdated packages
pip list --outdated

# Install from requirements file
pip install -r requirements.txt

# Freeze current environment to requirements
pip freeze > requirements.txt
```

## ⚡ Useful Shell Commands

```bash
# Enter Django shell
python manage.py shell

# Then run:
from accounts.models import CustomUser
users = CustomUser.objects.all()
user = CustomUser.objects.get(email='test@example.com')
user.role = 'exec'
user.save()
CustomUser.objects.filter(role='member').count()
```

## 🔐 Security

```bash
# Generate new SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Check security issues
python manage.py check --deploy

# Collect static files (production)
python manage.py collectstatic
```

## 📝 Useful Combinations

```bash
# Create migrations, migrate, and create superuser
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Run migrations and tests
python manage.py migrate
python manage.py test

# Full reset (dangerous!)
python manage.py flush --no-input
python manage.py migrate
python manage.py createsuperuser
```

## 🔧 Troubleshooting

**Models not showing in admin:**
```bash
# Add to app/admin.py and restart server
from django.contrib import admin
from .models import YourModel

admin.site.register(YourModel)
```

**Migrations not creating:**
```bash
# Ensure you're in the right directory
cd backend
python manage.py makemigrations
```

**Port 8000 already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
python manage.py runserver 8001
```

**Module import errors:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📚 More Info

Full Django documentation: https://docs.djangoproject.com/
Django REST Framework: https://www.django-rest-framework.org/
