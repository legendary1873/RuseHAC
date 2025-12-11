/**
 * RuseHAC Frontend Server
 * 
 * Serves the React frontend application with proper CORS and proxy support
 * Usage: node index.js [--prod]
 * 
 * Install dependencies:
 *   npm install express cors compression http-proxy-middleware dotenv
 */

const express = require('express');
const path = require('path');
const cors = require('cors');
const compression = require('compression');

let createProxyMiddleware;
try {
  createProxyMiddleware = require('http-proxy-middleware').createProxyMiddleware;
} catch {
  console.warn('⚠️  http-proxy-middleware not installed. API proxy will be disabled.');
  createProxyMiddleware = null;
}

const app = express();
const PORT = process.env.PORT || 3000;
const API_URL = process.env.API_URL || 'http://localhost:8000';
const NODE_ENV = process.argv.includes('--prod') ? 'production' : 'development';

// ============================================
// Middleware
// ============================================

// Compression
app.use(compression());

// CORS - Allow both localhost and production domains
const corsOptions = {
  origin: function (origin, callback) {
    const allowedOrigins = [
      'http://localhost:3000',
      'http://localhost:8000',
      'http://127.0.0.1:3000',
      'http://127.0.0.1:8000',
      // Add production domains here
      'https://rusehac.example.com',
    ];

    // Allow requests with no origin (mobile apps, curl requests)
    if (!origin || allowedOrigins.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
};

app.use(cors(corsOptions));

// Body parser
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ============================================
// API Proxy (Optional - requires http-proxy-middleware)
// ============================================

if (createProxyMiddleware) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: API_URL,
      changeOrigin: true,
      pathRewrite: {
        '^/api': '/api',
      },
      onError: (err, req, res) => {
        console.error('Proxy error:', err);
        res.status(503).json({
          error: 'Backend service unavailable',
          message: `Could not connect to API at ${API_URL}`,
        });
      },
    })
  );
}

// ============================================
// Static Files
// ============================================

// Serve public directory
const publicDir = path.join(__dirname, 'public');
app.use(express.static(publicDir));

// ============================================
// SPA Fallback
// ============================================

// Serve app.html for all non-API routes (SPA fallback)
app.get(/^(?!.*\.(js|css|json|png|jpg|gif|svg|ico|webp|woff|woff2|ttf|eot)$).*$/, (req, res) => {
  res.sendFile(path.join(publicDir, 'app.html'), (err) => {
    if (err) {
      // Fallback to index.html if app.html doesn't exist
      res.sendFile(path.join(publicDir, 'index.html'));
    }
  });
});

// ============================================
// Error Handling
// ============================================

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal Server Error',
    message: NODE_ENV === 'development' ? err.message : 'An error occurred',
  });
});

app.use((req, res) => {
  res.status(404).json({ error: 'Not Found' });
});

// ============================================
// Start Server
// ============================================

app.listen(PORT, () => {
  console.log(`
╔══════════════════════════════════════╗
║       RuseHAC Frontend Server        ║
╚══════════════════════════════════════╝

🚀 Server running at http://localhost:${PORT}
📡 API URL: ${API_URL}
🔧 Environment: ${NODE_ENV}

${createProxyMiddleware ? '✅ API proxy enabled' : '⚠️  API proxy disabled (install http-proxy-middleware)'}

Open http://localhost:${PORT} in your browser!
  `);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  process.exit(0);
});