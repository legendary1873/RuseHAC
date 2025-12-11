# Frontend Testing Guide - RuseHAC

This guide covers testing the React frontend application against the Django REST API backend.

## 📋 Prerequisites

1. **Backend Running** - Django server on `http://localhost:8000`
2. **Frontend Running** - Express server on `http://localhost:3000`
3. **Test Data** - Run `python manage.py shell < test_api.py` to populate test data

## 🚀 Quick Start Testing

### Test Data Created by Backend

The `backend/test_api.py` script creates:

```
Users:
  - admin@example.com (Admin) - password: admin123
  - exec@example.com (Exec) - password: exec123
  - member@example.com (Member) - password: member123

Announcements:
  - 2 announcements (1 pinned)

Meetings:
  - 3 meetings with attendance records

Shop:
  - 5 items (2-20 points)
  - 3 orders with different statuses

Ballots:
  - 2 ballots with 3-4 options each
  - Various votes cast

Exec Applications:
  - 1 pending application
```

## 🧪 Test Scenarios

### 1. Authentication Flow

**Objective**: Verify login/register/logout works

1. Open `http://localhost:3000`
2. Click "Register" tab
3. Fill in:
   - Email: `testuser@example.com`
   - First Name: `Test`
   - Last Name: `User`
   - Year Group: `Y10`
   - Password: `testpass123`
4. Click "Register"
5. ✅ Should redirect to dashboard
6. ✅ Should display username in navbar
7. Click "Logout"
8. ✅ Should redirect to login screen

**Test Login (with existing user)**:
1. Go to login tab
2. Email: `member@example.com`
3. Password: `member123`
4. ✅ Should show dashboard with user info

### 2. Dashboard

**Objective**: Verify dashboard displays user info and attendance

After logging in as `member@example.com`:

1. ✅ Profile card shows:
   - Role: `member`
   - Year Group: `Y10` (or whatever was set)
   - Points balance

2. ✅ Attendance card shows:
   - Attended/Total meetings
   - Percentage (should be 1/3 = 33.3%)
   - Target (70%)
   - "Need to attend more" warning

3. ✅ Announcements show:
   - Latest announcements
   - Pinned badge for pinned announcements
   - Author name

### 3. Voting

**Objective**: Verify ballot display and voting

1. Click "Voting" in navbar
2. ✅ Should display 2 ballots
3. ✅ Each ballot shows:
   - Title and description
   - All options with vote counts
   - Status (open/closed)

4. Cast a vote:
   - Click on an option button
   - Button should turn green (voted state)
   - Vote count should increase by 1

5. Try voting again:
   - Should be able to change vote
   - Old vote count decreases, new vote count increases

### 4. Shop

**Objective**: Verify shop display and item claiming

After logging in:

1. Click "Shop" in navbar
2. ✅ Current points displayed
3. ✅ Items grid shows:
   - Item name
   - Description
   - Point cost
   - Claim button (green if affordable, gray if insufficient points)

4. Claim an item:
   - Click "Claim" on 2-point item
   - ✅ Should show "Item claimed! Awaiting approval"
   - Points balance should update after approval

### 5. Chat (if implemented)

**Objective**: Verify real-time chat functionality

1. Need two browser tabs/windows with different users logged in
2. Go to Chat page
3. Select a chat room
4. User 1: Type message and send
5. ✅ User 2 should see message appear immediately
6. ✅ Message shows sender name and timestamp
7. Status indicator shows "Connected"

## 🔍 API Testing

### Using Browser Developer Tools

1. Open DevTools (F12)
2. Go to Network tab
3. Perform actions (login, vote, etc.)
4. Inspect requests and responses

**Example - Login Request**:
```
POST http://localhost:8000/api/accounts/token/
{
  "username": "member@example.com",
  "password": "member123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 2,
    "full_name": "Member User",
    "email": "member@example.com",
    "role": "member",
    "points": 100,
    ...
  }
}
```

### Using cURL (Terminal)

```bash
# Test API is running
curl http://localhost:8000/api/accounts/token/

# Login
curl -X POST http://localhost:8000/api/accounts/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"member@example.com","password":"member123"}'

# Get announcements (replace TOKEN with actual token)
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/core/announcements/

# Cast a vote
curl -X POST http://localhost:8000/api/ballots/votes/cast_vote/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ballot_id": 1, "option_id": 1}'
```

### Using Postman

1. Import API endpoints from `FEATURES_IMPLEMENTED.md`
2. Set up environment variables:
   - `base_url`: `http://localhost:8000/api`
   - `access_token`: (from login response)
3. Test each endpoint with provided request bodies

## ✅ Feature Checklist

### Authentication (10/10)
- ✅ Register new user
- ✅ Login with email/password
- ✅ Logout
- ✅ Auto-logout on 401
- ✅ Token refresh on expiry
- ✅ LocalStorage token persistence
- ✅ Year group selection
- ✅ Password validation
- ✅ Email validation
- ✅ Unique email constraint

### Dashboard (8/8)
- ✅ Display user profile
- ✅ Show role and year group
- ✅ Display points balance
- ✅ Show attendance stats
- ✅ Calculate attendance percentage
- ✅ Show 70% target status
- ✅ List latest announcements
- ✅ Show pinned announcements

### Voting (6/6)
- ✅ List all ballots
- ✅ Display ballot options
- ✅ Show vote counts
- ✅ Cast vote
- ✅ Change vote
- ✅ View voting history

### Shop (5/5)
- ✅ List shop items
- ✅ Display point costs
- ✅ Show current balance
- ✅ Claim items
- ✅ Disable claiming if insufficient points

### Chat (3/3)
- ✅ Connect to WebSocket
- ✅ Send/receive messages
- ✅ Show online status

## 🐛 Common Issues & Fixes

### Issue: CORS Error on API Requests

**Symptoms**: Browser console shows "Access to XMLHttpRequest has been blocked by CORS policy"

**Fix**:
1. Verify backend `ALLOWED_HOSTS` includes frontend URL
2. Verify `API_URL` environment variable is correct
3. Check Express CORS middleware is enabled
4. Restart both frontend and backend

```bash
# In backend
python manage.py runserver

# In new terminal
npm run dev  # Frontend
```

### Issue: "Cannot connect to backend" Error

**Symptoms**: Frontend shows "Backend service unavailable"

**Fix**:
1. Verify Django is running on `http://localhost:8000`
2. Check API proxy in Express: `http://localhost:3000/api/accounts/token/`
3. Check environment variable: `API_URL=http://localhost:8000`

### Issue: Tokens not persisting across page refresh

**Symptoms**: User gets logged out after F5 refresh

**Fix**:
1. Check localStorage in DevTools (F12 → Application → Local Storage)
2. Tokens should be stored as `access_token` and `refresh_token`
3. Check auth context initialization (should fetch user on mount)

### Issue: Chat WebSocket won't connect

**Symptoms**: Chat shows "🔴 Disconnected" status

**Fix**:
1. Verify backend Channels is configured: `ASGI_APPLICATION = 'config.asgi.application'`
2. Check WebSocket URL: Should be `ws://localhost:8000/ws/chat/...`
3. Verify auth token is passed to WebSocket
4. Check browser supports WebSocket (all modern browsers do)

## 📊 Performance Testing

### Metrics to Monitor

1. **Page Load Time**
   - DevTools Network tab → Finish time
   - Goal: < 2 seconds for initial load

2. **API Response Time**
   - DevTools Network tab → Time field
   - Goal: < 500ms per request

3. **Bundle Size**
   - Check `app_v2.jsx` size
   - Goal: < 100KB (minified)

### Load Testing

Test with multiple concurrent users:

```bash
# Using Apache Bench (if installed)
ab -n 100 -c 10 http://localhost:3000/

# Using wrk (if installed)
wrk -t4 -c100 -d30s http://localhost:3000/
```

## 🚀 Testing Deployment

### Local Production Mode

```bash
# Stop development server (Ctrl+C)
npm run prod
# Visit http://localhost:3000
```

### Using Docker (if set up)

```bash
docker build -t rusehac-frontend .
docker run -p 3000:3000 -e API_URL=http://localhost:8000 rusehac-frontend
```

## 📝 Test Results Template

Use this template to document test results:

```
Date: YYYY-MM-DD
Tester: Your Name
Frontend Version: 1.0.0
Backend Version: 1.0.0

✅ = Passed
❌ = Failed
🟡 = Partial

Authentication:
  ✅ Register new user
  ✅ Login existing user
  ...

Dashboard:
  ✅ Display user profile
  ...

Voting:
  ✅ List ballots
  ...

Shop:
  ✅ List items
  ...

Chat:
  ✅ Connect to WebSocket
  ...

Issues Found:
1. [Issue description]
2. [Issue description]

Notes:
- [Any additional observations]
```

## 🔗 Related Documentation

- [Backend API Documentation](backend/FEATURES_IMPLEMENTED.md)
- [Backend Setup](backend/README.md)
- [Frontend Setup](FRONTEND_SETUP.md)
- [Architecture Overview](ARCHITECTURE.md)

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review backend logs: `python manage.py runserver --verbosity 2`
3. Check browser console for JavaScript errors
4. Check Network tab for failed API requests
