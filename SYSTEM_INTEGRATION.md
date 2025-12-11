# RuseHAC Complete System Integration Guide

## System Overview

RuseHAC is a complete web platform consisting of:

1. **Frontend** - React SPA served by Express.js
2. **Backend** - Django REST API with WebSocket support
3. **Database** - SQLite (dev) / PostgreSQL (prod)
4. **Real-time** - Django Channels for WebSockets

This guide shows how all components work together.

## Complete Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        User's Browser                          │
│  (http://localhost:3000)                                      │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│              Express.js Frontend Server                         │
│              (Port 3000)                                        │
│                                                                 │
│  • Serves React SPA (public/js/app_v2.jsx)                    │
│  • Proxies /api/* → http://localhost:8000/api               │
│  • Handles CORS automatically                                  │
│  • Compresses responses with gzip                              │
└────────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────┐
        │    REST API & WebSocket Proxy       │
        │  (/api/*, /ws/*)                    │
        └─────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│            Django REST API Server                              │
│            (Port 8000)                                         │
│                                                                 │
│  REST Endpoints:                                               │
│  • /api/accounts/      - JWT auth, users, profiles            │
│  • /api/core/          - Announcements, meetings              │
│  • /api/ballots/       - Voting system                         │
│  • /api/shop/          - Points, items, orders                │
│  • /api/chat/          - Chat rooms, messages                 │
│  • /api/notifications/ - Alerts, subscriptions                │
│  • /api/resources/     - File uploads, essays                 │
│                                                                 │
│  WebSocket Endpoints:                                          │
│  • /ws/chat/{room_id}/ - Real-time messaging                  │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│              PostgreSQL Database                               │
│              (or SQLite for dev)                               │
│                                                                 │
│  Tables:                                                       │
│  • CustomUser         - User accounts with roles              │
│  • Announcement       - Club news                              │
│  • Meeting           - Event attendance                        │
│  • Ballot            - Voting system                           │
│  • ShopItem          - Merchandise                             │
│  • Order             - Purchase requests                       │
│  • ChatRoom          - Discussion channels                     │
│  • ChatMessage       - Messages                                │
│  • Notification      - Alerts                                  │
│  • Resource          - Shared files                            │
│  • Submission        - User essays                             │
│  • ExecApplication   - Role requests                           │
└────────────────────────────────────────────────────────────────┘
```

## Request Flow Examples

### Example 1: User Login

```
1. USER BROWSER
   ┌─ Opens http://localhost:3000
   └─ Sees Login form

2. USER INTERACTIONS
   ┌─ Enters email: member@example.com
   ├─ Enters password: member123
   └─ Clicks "Login"

3. FRONTEND (React)
   ┌─ Calls AuthAPI.login(email, password)
   ├─ Sends POST request to /api/accounts/token/
   └─ With body: {"username": "member@example.com", "password": "member123"}

4. EXPRESS SERVER
   ┌─ Receives POST /api/accounts/token/
   ├─ Proxies to http://localhost:8000/api/accounts/token/
   └─ Waits for Django response

5. DJANGO BACKEND
   ┌─ Receives POST request
   ├─ Validates credentials
   ├─ Looks up CustomUser in database
   ├─ Generates JWT tokens (access + refresh)
   ├─ Returns JSON with tokens + user data
   └─ Response:
      {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "user": {
          "id": 2,
          "full_name": "Member User",
          "email": "member@example.com",
          "role": "member",
          "year_group": "Y10",
          "points": 100
        }
      }

6. EXPRESS SERVER
   ┌─ Receives response from Django
   ├─ Proxies response back to browser
   └─ (No modifications)

7. FRONTEND (React)
   ┌─ Receives token response
   ├─ Stores access_token in localStorage
   ├─ Stores refresh_token in localStorage
   ├─ Updates AuthContext with user data
   ├─ Redirects to /dashboard
   └─ Displays "Welcome, Member User!"

8. RESULT
   ✅ User logged in
   ✅ Tokens stored locally
   ✅ API requests include "Authorization: Bearer {token}"
```

### Example 2: Casting a Vote

```
1. USER INTERACTIONS
   ┌─ Views ballot "What should be our next trip?"
   ├─ Option 1: "London" (50 votes)
   ├─ Option 2: "Paris" (45 votes)
   └─ Clicks "London" button

2. FRONTEND (React)
   ┌─ Sends POST to /api/ballots/votes/cast_vote/
   ├─ With token: Authorization: Bearer {access_token}
   ├─ With body:
   │  {
   │    "ballot_id": 1,
   │    "option_id": 1
   │  }
   └─ Updates UI optimistically (button turns green)

3. EXPRESS SERVER
   ┌─ Receives POST /api/ballots/votes/cast_vote/
   ├─ Sees Authorization header
   ├─ Proxies to Django with all headers
   └─ Waits for response

4. DJANGO BACKEND
   ┌─ Receives POST request
   ├─ Extracts JWT token from Authorization header
   ├─ Validates JWT (signature, expiry, user)
   ├─ Identifies user from token (user_id: 2)
   ├─ Checks if user already voted (finds old vote)
   ├─ Deletes old vote for option 2
   ├─ Creates new Vote record:
   │  Vote(user_id=2, ballot_id=1, option_id=1)
   ├─ Recalculates option vote counts
   ├─ Returns response:
   │  {
   │    "id": 123,
   │    "ballot_id": 1,
   │    "option_id": 1,
   │    "option_text": "London",
   │    "vote_count": 51  // Updated!
   │  }
   └─ Updates Vote and BallotOption in database

5. EXPRESS SERVER
   ┌─ Receives response (51 votes)
   └─ Proxies back to frontend

6. FRONTEND (React)
   ┌─ Receives updated vote count
   ├─ Updates "London" button to show 51 votes
   ├─ Updates ballot state
   └─ User sees green button with "51" votes

7. DATABASE STATE
   ┌─ Vote table has new row with member's vote
   └─ BallotOption has updated vote_count

8. RESULT
   ✅ Vote recorded
   ✅ UI updated immediately
   ✅ Vote count correct
   ✅ Can change vote anytime
```

### Example 3: Real-time Chat

```
1. USER OPENS CHAT
   ┌─ Clicks "Chat" in navbar
   ├─ Selects room "General Discussion"
   └─ Chat component initializes

2. FRONTEND (React)
   ┌─ Calls ChatManager.connect(room_id)
   ├─ Creates WebSocket connection:
   │  ws://localhost:8000/ws/chat/1/?token={access_token}
   └─ Waits for Django to accept connection

3. EXPRESS SERVER
   ┌─ Receives WebSocket upgrade request
   ├─ Proxies to Django backend
   └─ Django accepts and upgrades connection

4. DJANGO BACKEND (Channels)
   ┌─ ChatConsumer.connect() called
   ├─ Validates JWT token from query params
   ├─ Identifies user from token
   ├─ Joins user to room's WebSocket group
   │  ("chat_room_1" group)
   ├─ Sends welcome message
   ├─ Notifies others: "{user} joined"
   └─ Ready to receive/broadcast messages

5. REAL-TIME MESSAGING
   ┌─ User A types "Hello everyone!"
   ├─ Clicks Send
   │
   ├─ FRONTEND: Sends via WebSocket
   │  {
   │    "type": "message",
   │    "message": "Hello everyone!"
   │  }
   │
   ├─ DJANGO: ChatConsumer.receive()
   │  ├─ Receives message
   │  ├─ Creates ChatMessage record in database
   │  ├─ Broadcasts to all in "chat_room_1" group:
   │  │  {
   │  │    "type": "message",
   │  │    "message": "Hello everyone!",
   │  │    "sender": "Member User",
   │  │    "timestamp": "2024-01-15 14:30:45"
   │  │  }
   │  └─ ALL connected users receive message
   │
   ├─ USER B'S BROWSER: Receives via WebSocket
   │  ├─ ChatRoom component gets message
   │  ├─ Updates messages[] state
   │  └─ Message appears immediately on screen
   │
   ├─ DATABASE: ChatMessage stored
   │  ChatMessage(room_id=1, sender_id=2, message="Hello everyone!")
   │
   └─ RESULT: ✅ Instant delivery to all users

6. MESSAGE HISTORY
   ┌─ User C joins room later
   ├─ Sends request for room history
   ├─ Django sends last 50 messages
   ├─ User C sees full conversation
   └─ Can continue chatting
```

## Security & Authentication Flow

```
LOGIN PROCESS
├─ User submits credentials
├─ Backend creates JWT tokens:
│  ├─ access_token (15 min expiry)
│  └─ refresh_token (7 day expiry)
├─ Frontend stores in localStorage
└─ access_token sent with every request

PROTECTED REQUEST
├─ Frontend sends: Authorization: Bearer {access_token}
├─ Django verifies JWT signature
├─ Django checks expiry
├─ Django extracts user_id from token
├─ Request processed as authenticated user

TOKEN EXPIRY
├─ Backend returns 401 Unauthorized
├─ Frontend intercepts 401
├─ Frontend sends refresh request:
│  POST /api/accounts/token/refresh/
│  {"refresh": refresh_token}
├─ Backend validates refresh token
├─ Backend returns new access_token
├─ Frontend retries original request
└─ User never sees login page

LOGOUT
├─ Frontend clears localStorage tokens
├─ Future requests have no Authorization header
├─ Backend treats as anonymous
└─ Frontend redirects to login
```

## Database Relationships

```
CustomUser (Users)
├─ id (PK)
├─ email (unique)
├─ first_name, last_name
├─ role (member, exec, admin)
├─ year_group (Y7-Y13)
├─ points (default: 100)
└─ bio

  ↓ FK (author)
  
Announcement
├─ id (PK)
├─ author (FK → CustomUser)
├─ title
├─ content
├─ pinned (boolean)
└─ created_at

  ↓ FK (organizer)

Meeting
├─ id (PK)
├─ organizer (FK → CustomUser)
├─ title
├─ date
├─ location
└─ created_at

  ↓ FK (attendee, meeting)

Attendance
├─ id (PK)
├─ attendee (FK → CustomUser)
├─ meeting (FK → Meeting)
├─ attended (boolean)
└─ term (Sept-July year)

  ↓ FK (creator)

Ballot
├─ id (PK)
├─ creator (FK → CustomUser)
├─ title
├─ description
├─ is_open (boolean)
├─ deadline
└─ created_at

  ↓ FK (ballot)

BallotOption
├─ id (PK)
├─ ballot (FK → Ballot)
├─ text
└─ vote_count (cached)

  ↓ FK (ballot, voter, option)

Vote
├─ id (PK)
├─ ballot (FK → Ballot)
├─ voter (FK → CustomUser)
├─ option (FK → BallotOption)
├─ unique_together(ballot, voter)
└─ created_at

  ↓ FK (user)

ShopItem
├─ id (PK)
├─ name
├─ description
├─ cost (points)
├─ quantity_available
└─ created_at

  ↓ FK (item, user)

Order
├─ id (PK)
├─ item (FK → ShopItem)
├─ user (FK → CustomUser)
├─ quantity
├─ status (pending/approved/claimed/rejected)
└─ created_at

  ↓ FK (user)

PointTransaction
├─ id (PK)
├─ user (FK → CustomUser)
├─ points (amount)
├─ reason (why points awarded)
├─ transaction_type (award, spend)
└─ created_at

  ↓ FK (creator)

ChatRoom
├─ id (PK)
├─ name
├─ description
├─ created_by (FK → CustomUser)
└─ created_at

  ↓ FK (room, sender)

ChatMessage
├─ id (PK)
├─ room (FK → ChatRoom)
├─ sender (FK → CustomUser)
├─ message (text)
└─ timestamp

  ↓ FK (user, app)

ExecApplication
├─ id (PK)
├─ user (FK → CustomUser)
├─ applied_role (member→exec)
├─ status (pending/approved/rejected)
├─ reason_if_rejected (text)
└─ applied_at
```

## API Request/Response Examples

### Authentication - Login
```http
POST /api/accounts/token/
Content-Type: application/json

{
  "username": "member@example.com",
  "password": "member123"
}

Response 200:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 2,
    "email": "member@example.com",
    "full_name": "Member User",
    "role": "member",
    "points": 100,
    "year_group": "Y10",
    "gravatar_url": "https://www.gravatar.com/avatar/..."
  }
}
```

### Core - Get Announcements
```http
GET /api/core/announcements/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

Response 200:
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "title": "Welcome to RuseHAC!",
      "content": "This is our new platform...",
      "author": {
        "id": 1,
        "full_name": "Admin User",
        "gravatar_url": "..."
      },
      "pinned": true,
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### Ballots - Cast Vote
```http
POST /api/ballots/votes/cast_vote/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "ballot_id": 1,
  "option_id": 1
}

Response 201:
{
  "id": 123,
  "ballot_id": 1,
  "ballot_title": "Next Trip Destination?",
  "option_id": 1,
  "option_text": "London",
  "option_vote_count": 51,
  "created_at": "2024-01-15T14:30:45Z"
}
```

### Shop - Claim Item
```http
POST /api/shop/orders/claim_item/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "item_id": 2,
  "quantity": 1
}

Response 201:
{
  "id": 45,
  "item": {
    "id": 2,
    "name": "RuseHAC Sticker Pack",
    "cost": 10
  },
  "user": "member@example.com",
  "quantity": 1,
  "status": "pending",
  "created_at": "2024-01-15T14:35:00Z"
}
```

## Monitoring & Debugging

### Check Backend Logs
```bash
# Terminal running Django
python manage.py runserver
# Shows all requests:
# [15/Jan/2024 14:30:45] "POST /api/ballots/votes/cast_vote/ HTTP/1.1" 201 325
```

### Check Frontend Network
```
1. Open browser DevTools (F12)
2. Go to Network tab
3. Perform action (login, vote, etc.)
4. Click on request to see:
   - Headers (Authorization token)
   - Request body
   - Response
   - Status code (200, 201, 401, 500, etc.)
```

### Check WebSocket Connection
```
1. DevTools → Network tab
2. Filter: WS
3. Look for WebSocket connections
4. Click to see frames sent/received
5. Green indicator = connected
6. Red = disconnected/errored
```

## Testing Locally

### Test All Components Together

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python manage.py runserver
# → Logs show all API requests

# Terminal 2: Frontend
npm run dev
# → Logs show startup messages
# → Browser DevTools shows network requests

# Terminal 3: Test data
cd backend
python manage.py shell < test_api.py
# → Creates test users, announcements, votes, etc.

# Browser: http://localhost:3000
# Login: member@example.com / member123
# Test each feature
```

### Test API Directly

```bash
# Get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/accounts/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"member@example.com","password":"member123"}' \
  | jq -r '.access')

# Use token for requests
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/core/announcements/

# Cast a vote
curl -X POST http://localhost:8000/api/ballots/votes/cast_vote/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ballot_id": 1, "option_id": 1}'
```

## Deployment Checklist

- [ ] Backend
  - [ ] PostgreSQL configured
  - [ ] Environment variables set (.env)
  - [ ] SECRET_KEY configured
  - [ ] ALLOWED_HOSTS set
  - [ ] DEBUG = False
  - [ ] Migrations run
  - [ ] Static files collected
  - [ ] Email configured
  - [ ] Celery running (optional)
  - [ ] Redis running (optional)

- [ ] Frontend
  - [ ] API_URL points to production backend
  - [ ] NODE_ENV = production
  - [ ] PORT set (default 3000)
  - [ ] npm install --production
  - [ ] npm run prod started

- [ ] Infrastructure
  - [ ] HTTPS enabled
  - [ ] CORS configured
  - [ ] Rate limiting enabled
  - [ ] Backup strategy
  - [ ] Error logging
  - [ ] Performance monitoring

---

**This is the complete RuseHAC system working together. All components integrate seamlessly for a complete user experience.**

For next steps, see:
- [QUICKSTART.md](QUICKSTART.md) - Get running immediately
- [FRONTEND_TESTING.md](FRONTEND_TESTING.md) - Test all features
- [backend/FEATURES_IMPLEMENTED.md](backend/FEATURES_IMPLEMENTED.md) - API reference