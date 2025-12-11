#!/bin/bash
# Quick development startup script for RuseHAC

echo "🚀 Starting RuseHAC Development Server"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python -m venv venv"
    echo "Then: source venv/bin/activate"
    echo "Then: pip install -r requirements.txt"
    exit 1
fi

# Activate venv
source venv/bin/activate

# Check if packages are installed
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Django not installed!"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Virtual environment ready"
echo ""
echo "Starting Django server on http://localhost:8000..."
echo "Press Ctrl+C to stop"
echo ""

cd backend
python manage.py runserver
