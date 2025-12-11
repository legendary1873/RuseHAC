import React, { useState, useEffect, useContext, createContext } from 'react';
import axios from 'axios';

// Create Auth Context
const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

// API Client
const API_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercept requests to add token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Intercept responses to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refresh_token = localStorage.getItem('refresh_token');
      if (refresh_token) {
        try {
          const response = await axios.post(`${API_URL}/accounts/token/refresh/`, {
            refresh: refresh_token,
          });
          localStorage.setItem('access_token', response.data.access);
          apiClient.defaults.headers.common.Authorization = `Bearer ${response.data.access}`;
          return apiClient(originalRequest);
        } catch {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

// Auth Provider
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
      const response = await apiClient.get('/accounts/users/me/');
      setUser(response.data);
    } catch (error) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } finally {
      setLoading(false);
    }
  };

  const register = async (email, firstName, lastName, yearGroup, password) => {
    const response = await apiClient.post('/accounts/users/register/', {
      email,
      first_name: firstName,
      last_name: lastName,
      year_group: yearGroup,
      password,
      password2: password,
    });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    setUser(response.data.user);
    return response.data;
  };

  const login = async (email, password) => {
    const response = await apiClient.post('/accounts/token/', {
      username: email,
      password,
    });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    setUser(response.data.user);
    return response.data;
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, register, login, logout, apiClient }}>
      {children}
    </AuthContext.Provider>
  );
};

// Login Component
export const Login = ({ onLoginSuccess }) => {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(email, password);
      onLoginSuccess?.();
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-form">
      <h2>Login</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
};

// Register Component
export const Register = ({ onRegisterSuccess }) => {
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    firstName: '',
    lastName: '',
    yearGroup: 'Y10',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await register(
        formData.email,
        formData.firstName,
        formData.lastName,
        formData.yearGroup,
        formData.password
      );
      onRegisterSuccess?.();
    } catch (err) {
      setError(err.response?.data?.email?.[0] || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-form">
      <h2>Register</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="firstName"
          placeholder="First Name"
          value={formData.firstName}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="lastName"
          placeholder="Last Name"
          value={formData.lastName}
          onChange={handleChange}
          required
        />
        <select name="yearGroup" value={formData.yearGroup} onChange={handleChange}>
          <option value="Y7">Year 7</option>
          <option value="Y8">Year 8</option>
          <option value="Y9">Year 9</option>
          <option value="Y10">Year 10</option>
          <option value="Y11">Year 11</option>
          <option value="Y12">Year 12</option>
          <option value="Y13">Year 13</option>
        </select>
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
    </div>
  );
};

// Dashboard Component
export const Dashboard = () => {
  const { user, apiClient } = useAuth();
  const [announcements, setAnnouncements] = useState([]);
  const [attendance, setAttendance] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [announcementsRes, attendanceRes] = await Promise.all([
        apiClient.get('/core/announcements/'),
        apiClient.get('/core/attendance/my_stats/'),
      ]);
      setAnnouncements(announcementsRes.data.results || announcementsRes.data);
      setAttendance(attendanceRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      <h1>Welcome, {user?.full_name}!</h1>

      {/* User Info Card */}
      <div className="card">
        <h2>Profile</h2>
        <p>Role: {user?.role}</p>
        <p>Year Group: {user?.year_group}</p>
        <p>Points: {user?.points}</p>
      </div>

      {/* Attendance Card */}
      {attendance && (
        <div className="card">
          <h2>Term Attendance</h2>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${Math.min(attendance.percentage, 100)}%` }}
            >
              {attendance.percentage.toFixed(1)}%
            </div>
          </div>
          <p>
            Attended: {attendance.attended}/{attendance.total} meetings
          </p>
          <p>
            Target: {attendance.target_percentage}% ({attendance.remaining_needed} more needed)
          </p>
          <p className={attendance.on_target ? 'success' : 'warning'}>
            {attendance.on_target ? '✓ On track!' : '⚠️ Need to attend more meetings'}
          </p>
        </div>
      )}

      {/* Announcements */}
      <div className="card">
        <h2>Latest Announcements</h2>
        {announcements.slice(0, 5).map((ann) => (
          <div key={ann.id} className="announcement">
            {ann.pinned && <span className="badge">Pinned</span>}
            <h3>{ann.title}</h3>
            <p>{ann.content}</p>
            <small>By {ann.author_name}</small>
          </div>
        ))}
      </div>
    </div>
  );
};

// Voting Component
export const Voting = () => {
  const { apiClient } = useAuth();
  const [ballots, setBallots] = useState([]);
  const [userVotes, setUserVotes] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBallots();
  }, []);

  const fetchBallots = async () => {
    try {
      const response = await apiClient.get('/ballots/ballots/');
      setBallots(response.data.results || response.data);
      
      const votesRes = await apiClient.get('/ballots/votes/my_votes/');
      const votes = {};
      (votesRes.data.results || votesRes.data).forEach((vote) => {
        votes[vote.ballot] = vote.option;
      });
      setUserVotes(votes);
    } catch (error) {
      console.error('Error fetching ballots:', error);
    } finally {
      setLoading(false);
    }
  };

  const castVote = async (ballotId, optionId) => {
    try {
      await apiClient.post('/ballots/votes/cast_vote/', {
        ballot_id: ballotId,
        option_id: optionId,
      });
      setUserVotes({ ...userVotes, [ballotId]: optionId });
    } catch (error) {
      console.error('Error casting vote:', error);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="voting">
      <h1>Voting</h1>
      {ballots.map((ballot) => (
        <div key={ballot.id} className="card ballot">
          <h2>{ballot.title}</h2>
          <p>{ballot.description}</p>
          {ballot.is_open ? (
            <div>
              <p>Votes cast: {ballot.vote_count}</p>
              {ballot.options.map((option) => (
                <button
                  key={option.id}
                  className={userVotes[ballot.id] === option.id ? 'voted' : ''}
                  onClick={() => castVote(ballot.id, option.id)}
                >
                  {option.text} ({option.vote_count})
                </button>
              ))}
            </div>
          ) : (
            <p className="closed">Ballot closed</p>
          )}
        </div>
      ))}
    </div>
  );
};

// Shop Component
export const Shop = () => {
  const { user, apiClient } = useAuth();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchShopItems();
  }, []);

  const fetchShopItems = async () => {
    try {
      const response = await apiClient.get('/shop/items/');
      setItems(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching shop items:', error);
    } finally {
      setLoading(false);
    }
  };

  const claimItem = async (itemId) => {
    try {
      await apiClient.post('/shop/orders/claim_item/', {
        item_id: itemId,
        quantity: 1,
      });
      alert('Item claimed! Awaiting approval.');
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to claim item');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="shop">
      <h1>Shop</h1>
      <p>Your points: {user?.points}</p>
      <div className="items-grid">
        {items.map((item) => (
          <div key={item.id} className="card item">
            <h3>{item.name}</h3>
            <p>{item.description}</p>
            <p className="cost">{item.cost} points</p>
            {user && user.points >= item.cost ? (
              <button onClick={() => claimItem(item.id)}>Claim</button>
            ) : (
              <button disabled>Insufficient points</button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

// Main App Component
export default function App() {
  const { user, loading } = useAuth();
  const [currentPage, setCurrentPage] = useState('dashboard');

  if (loading) return <div className="loading">Loading...</div>;

  if (!user) {
    return (
      <div className="container">
        <Login onLoginSuccess={() => setCurrentPage('dashboard')} />
        <div className="divider">or</div>
        <Register onRegisterSuccess={() => setCurrentPage('dashboard')} />
      </div>
    );
  }

  const pages = {
    dashboard: <Dashboard />,
    voting: <Voting />,
    shop: <Shop />,
  };

  return (
    <div className="app">
      <nav className="navbar">
        <h1>🏛️ RuseHAC</h1>
        <div className="nav-links">
          <button onClick={() => setCurrentPage('dashboard')} className={currentPage === 'dashboard' ? 'active' : ''}>
            Dashboard
          </button>
          <button onClick={() => setCurrentPage('voting')} className={currentPage === 'voting' ? 'active' : ''}>
            Voting
          </button>
          <button onClick={() => setCurrentPage('shop')} className={currentPage === 'shop' ? 'active' : ''}>
            Shop
          </button>
        </div>
        <div className="user-menu">
          <span>{user?.full_name}</span>
          <button onClick={() => {
            const { logout } = useAuth();
            logout();
            setCurrentPage('dashboard');
          }}>
            Logout
          </button>
        </div>
      </nav>
      <main className="main-content">
        {pages[currentPage] || pages['dashboard']}
      </main>
    </div>
  );
}
