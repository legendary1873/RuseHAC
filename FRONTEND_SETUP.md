# RuseHAC Frontend - Setup & Usage Guide

This is the React frontend for the RuseHAC (History Club) web application. The frontend is served by an Express server and communicates with the Django REST API backend.

## 📋 Requirements

- Node.js 14+ 
- npm or yarn
- Backend API running on `http://localhost:8000` (see backend requirements)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

This installs:
- `express` - Web server
- `cors` - Cross-origin resource sharing
- `compression` - Response compression
- `http-proxy-middleware` - API proxy
- `dotenv` - Environment variables

### 2. Start the Backend

Before running the frontend, ensure the Django backend is running:

```bash
cd backend
python manage.py runserver
```

The API should be available at `http://localhost:8000/api`

### 3. Start the Frontend Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📝 Available Scripts

```bash
# Development mode (with API proxy to http://localhost:8000)
npm run dev

# Development with file watching (requires nodemon)
npm run dev:watch

# Production mode
npm run prod

# Start with custom API URL
API_URL=https://api.example.com node index.js
```

## 🏗️ Project Structure

```
public/
  ├── index.html          # Original static HTML
  ├── app.html           # React SPA entry point
  ├── js/
  │   ├── app.js         # Original vanilla JS
  │   └── app_v2.jsx     # React components (NEW)
  └── css/
      ├── style.css      # Original styles
      └── app.css        # React styles (NEW)

index.js                  # Express server with API proxy
package.json             # Node dependencies
```

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
PORT=3000
API_URL=http://localhost:8000
NODE_ENV=development
```

## 🌐 Frontend Components

The React application includes the following pages/features:

### Authentication
- **Login** - Sign in with email and password
- **Register** - Create new account with email, name, year group
- Auto token refresh using refresh tokens

### Dashboard
- Welcome message with user name
- Profile information (role, year group, points)
- Term attendance tracking with 70% target calculation
- Latest announcements feed

### Voting
- View all active ballots
- Cast votes on ballot options
- See vote counts in real-time
- View voting history

### Shop
- Browse merchandise items
- View point costs
- Claim items (with point approval workflow)
- Display current points balance

## 🔐 Authentication Flow

1. User logs in/registers with email and password
2. Backend returns `access_token` and `refresh_token`
3. Tokens stored in localStorage
4. `access_token` sent with all API requests in Authorization header
5. When access token expires, `refresh_token` used to get new token
6. Invalid refresh token redirects to login

## 🌊 API Proxy

The Express server proxies all `/api` requests to the Django backend at `http://localhost:8000`.

Example:
- Frontend request: `GET /api/accounts/users/me/`
- Proxied to: `GET http://localhost:8000/api/accounts/users/me/`

CORS is automatically handled by the proxy middleware.

## 📱 Responsive Design

The frontend uses CSS Grid and Flexbox for responsive layout:
- Mobile: Single column, stacked navigation
- Tablet: 2-column grid for items
- Desktop: Multi-column layouts with side-by-side forms

## 🐛 Troubleshooting

### "Cannot GET /"
- Ensure `app.html` exists in the `public/` directory
- Check that Express is serving static files correctly

### API requests fail with CORS error
- Verify backend is running on `http://localhost:8000`
- Check `API_URL` environment variable matches backend URL
- Ensure backend has CORS enabled in Django settings

### "Module not found" errors
- Run `npm install` to ensure all dependencies are installed
- Check that Node version is 14+

### Port already in use
- Change PORT: `PORT=3001 npm run dev`
- Or kill existing process: `lsof -ti:3000 | xargs kill -9`

## 🔄 Backend API Integration

The frontend expects the following API endpoints:

### Authentication
- `POST /api/accounts/token/` - Login with username/password
- `POST /api/accounts/token/refresh/` - Refresh access token
- `POST /api/accounts/users/register/` - Register new user
- `GET /api/accounts/users/me/` - Get current user profile

### Core (Announcements/Attendance)
- `GET /api/core/announcements/` - List announcements
- `GET /api/core/attendance/my_stats/` - Get attendance stats

### Voting
- `GET /api/ballots/ballots/` - List ballots
- `GET /api/ballots/votes/my_votes/` - Get user's votes
- `POST /api/ballots/votes/cast_vote/` - Cast a vote

### Shop
- `GET /api/shop/items/` - List shop items
- `POST /api/shop/orders/claim_item/` - Claim a merchandise item

## 🚢 Deployment

### Using npm (simple)
```bash
npm run prod
```

### Using PM2 (recommended for production)
```bash
npm install -g pm2
pm2 start index.js --name rusehac-frontend
pm2 save
pm2 startup
```

### Using Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY public/ ./public/
COPY index.js .
EXPOSE 3000
CMD ["npm", "run", "prod"]
```

Build and run:
```bash
docker build -t rusehac-frontend .
docker run -p 3000:3000 -e API_URL=https://api.example.com rusehac-frontend
```

## 📊 Performance Optimization

Current optimizations:
- ✅ Gzip compression enabled
- ✅ CSS/JS minification via CDN
- ✅ Token refresh prevents re-login
- ✅ Lazy loading announcements

Potential improvements:
- [ ] Code splitting for different pages
- [ ] Service worker for offline support
- [ ] Caching strategy for API responses
- [ ] Image optimization

## 🧪 Testing

To test the frontend:

1. Ensure backend is running
2. Ensure frontend is running at http://localhost:3000
3. Test login with credentials:
   - Email: `admin@example.com` (or any user created via Django admin)
   - Password: (use test data from `backend/test_api.py`)

## 📚 Related Documentation

- [Backend Setup](../backend/README.md)
- [API Endpoints](../backend/FEATURES_IMPLEMENTED.md)
- [Deployment Guide](../DEPLOYMENT.md)
- [Architecture Overview](../ARCHITECTURE.md)

## ❓ FAQ

**Q: Can I run this without Node.js?**
A: No, Node.js is required to run the Express server. You could serve static files with any HTTP server, but you'd lose the API proxy functionality.

**Q: Why use Express instead of Create React App?**
A: Express provides better control over CORS, API proxying, and deployment. It's production-ready and lightweight.

**Q: How do I handle real-time updates (chat, notifications)?**
A: The backend has WebSocket support via Django Channels. The frontend would need a WebSocket client (socket.io) to connect. This is planned for Phase 3.

**Q: Can I deploy frontend and backend separately?**
A: Yes! Set the `API_URL` environment variable to your production backend URL when deploying.
