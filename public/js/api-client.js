/**
 * API Client Utilities for RuseHAC Frontend
 * 
 * Provides typed API methods for all backend endpoints
 */

// Base API configuration
export const API_CONFIG = {
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};

/**
 * API Client with automatic token management
 */
export class APIClient {
  constructor() {
    this.baseURL = API_CONFIG.baseURL;
    this.accessToken = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token');
  }

  /**
   * Get request headers with auth token
   */
  getHeaders(additionalHeaders = {}) {
    return {
      ...API_CONFIG.headers,
      ...(this.accessToken && {
        Authorization: `Bearer ${this.accessToken}`,
      }),
      ...additionalHeaders,
    };
  }

  /**
   * Make HTTP request with automatic token refresh
   */
  async request(method, endpoint, data = null, headers = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const options = {
      method,
      headers: this.getHeaders(headers),
      ...(data && { body: JSON.stringify(data) }),
    };

    try {
      const response = await fetch(url, options);

      if (response.status === 401 && this.refreshToken) {
        // Token expired, try to refresh
        await this.refreshAccessToken();
        options.headers = this.getHeaders(headers);
        return fetch(url, options);
      }

      if (!response.ok) {
        throw new Error(`${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error [${method} ${endpoint}]:`, error);
      throw error;
    }
  }

  /**
   * Refresh access token using refresh token
   */
  async refreshAccessToken() {
    try {
      const response = await fetch(`${this.baseURL}/accounts/token/refresh/`, {
        method: 'POST',
        headers: API_CONFIG.headers,
        body: JSON.stringify({ refresh: this.refreshToken }),
      });

      const data = await response.json();
      this.accessToken = data.access;
      localStorage.setItem('access_token', data.access);
    } catch (error) {
      console.error('Token refresh failed:', error);
      // Redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
  }

  /**
   * GET request
   */
  get(endpoint, headers = {}) {
    return this.request('GET', endpoint, null, headers);
  }

  /**
   * POST request
   */
  post(endpoint, data, headers = {}) {
    return this.request('POST', endpoint, data, headers);
  }

  /**
   * PUT request
   */
  put(endpoint, data, headers = {}) {
    return this.request('PUT', endpoint, data, headers);
  }

  /**
   * PATCH request
   */
  patch(endpoint, data, headers = {}) {
    return this.request('PATCH', endpoint, data, headers);
  }

  /**
   * DELETE request
   */
  delete(endpoint, headers = {}) {
    return this.request('DELETE', endpoint, null, headers);
  }
}

/**
 * Authentication API methods
 */
export const AuthAPI = {
  /**
   * Register new user
   */
  register: (email, firstName, lastName, yearGroup, password) =>
    new APIClient().post('/accounts/users/register/', {
      email,
      first_name: firstName,
      last_name: lastName,
      year_group: yearGroup,
      password,
      password2: password,
    }),

  /**
   * Login with email/password
   */
  login: (username, password) =>
    new APIClient().post('/accounts/token/', { username, password }),

  /**
   * Get current user profile
   */
  getProfile: () => new APIClient().get('/accounts/users/me/'),

  /**
   * Update user profile
   */
  updateProfile: (data) =>
    new APIClient().patch('/accounts/users/me/', data),

  /**
   * Change password
   */
  changePassword: (currentPassword, newPassword) =>
    new APIClient().post('/accounts/users/change_password/', {
      current_password: currentPassword,
      new_password: newPassword,
    }),

  /**
   * Search users by name or email
   */
  searchUsers: (query) =>
    new APIClient().get(`/accounts/users/?search=${query}`),

  /**
   * Get user by ID
   */
  getUser: (id) => new APIClient().get(`/accounts/users/${id}/`),
};

/**
 * Core API methods (Announcements, Meetings, Attendance)
 */
export const CoreAPI = {
  /**
   * Get all announcements
   */
  getAnnouncements: () => new APIClient().get('/core/announcements/'),

  /**
   * Create announcement (exec only)
   */
  createAnnouncement: (title, content) =>
    new APIClient().post('/core/announcements/', { title, content }),

  /**
   * Pin announcement (exec only)
   */
  pinAnnouncement: (id) =>
    new APIClient().post(`/core/announcements/${id}/pin/`, {}),

  /**
   * Unpin announcement (exec only)
   */
  unpinAnnouncement: (id) =>
    new APIClient().post(`/core/announcements/${id}/unpin/`, {}),

  /**
   * Get all meetings
   */
  getMeetings: () => new APIClient().get('/core/meetings/'),

  /**
   * Create meeting (exec only)
   */
  createMeeting: (title, date, location) =>
    new APIClient().post('/core/meetings/', { title, date, location }),

  /**
   * Mark attendance for a meeting (exec only)
   */
  markAttendance: (meetingId, attendees) =>
    new APIClient().post(`/core/meetings/${meetingId}/mark_attendance/`, {
      attendees,
    }),

  /**
   * Get user attendance stats
   */
  getAttendanceStats: () =>
    new APIClient().get('/core/attendance/my_stats/'),

  /**
   * Get attendance leaderboard
   */
  getLeaderboard: () =>
    new APIClient().get('/core/attendance/leaderboard/'),
};

/**
 * Shop API methods
 */
export const ShopAPI = {
  /**
   * Get all shop items
   */
  getItems: () => new APIClient().get('/shop/items/'),

  /**
   * Get shop item by ID
   */
  getItem: (id) => new APIClient().get(`/shop/items/${id}/`),

  /**
   * Create shop item (exec only)
   */
  createItem: (name, description, cost) =>
    new APIClient().post('/shop/items/', {
      name,
      description,
      cost,
    }),

  /**
   * Get point transactions
   */
  getTransactions: () =>
    new APIClient().get('/shop/point-transactions/'),

  /**
   * Award points to users (exec only)
   */
  awardPoints: (userId, points, reason) =>
    new APIClient().post('/shop/point-transactions/award_points/', {
      user_id: userId,
      points,
      reason,
    }),

  /**
   * Get user's orders
   */
  getOrders: () => new APIClient().get('/shop/orders/'),

  /**
   * Claim an item
   */
  claimItem: (itemId, quantity = 1) =>
    new APIClient().post('/shop/orders/claim_item/', {
      item_id: itemId,
      quantity,
    }),

  /**
   * Approve order (exec only)
   */
  approveOrder: (orderId) =>
    new APIClient().post(`/shop/orders/${orderId}/approve/`, {}),

  /**
   * Reject order (exec only)
   */
  rejectOrder: (orderId, reason) =>
    new APIClient().post(`/shop/orders/${orderId}/reject/`, { reason }),

  /**
   * Mark order as claimed
   */
  markClaimed: (orderId) =>
    new APIClient().post(`/shop/orders/${orderId}/mark_claimed/`, {}),
};

/**
 * Ballot API methods
 */
export const BallotAPI = {
  /**
   * Get all ballots
   */
  getBallots: () => new APIClient().get('/ballots/ballots/'),

  /**
   * Get ballot by ID
   */
  getBallot: (id) => new APIClient().get(`/ballots/ballots/${id}/`),

  /**
   * Create ballot (exec only)
   */
  createBallot: (title, description, deadline) =>
    new APIClient().post('/ballots/ballots/', {
      title,
      description,
      deadline,
    }),

  /**
   * Close ballot (exec only)
   */
  closeBallot: (id) =>
    new APIClient().post(`/ballots/ballots/${id}/close/`, {}),

  /**
   * Add option to ballot
   */
  addOption: (ballotId, text) =>
    new APIClient().post('/ballots/ballot-options/', {
      ballot_id: ballotId,
      text,
    }),

  /**
   * Cast a vote
   */
  castVote: (ballotId, optionId) =>
    new APIClient().post('/ballots/votes/cast_vote/', {
      ballot_id: ballotId,
      option_id: optionId,
    }),

  /**
   * Get user's votes
   */
  getUserVotes: () =>
    new APIClient().get('/ballots/votes/my_votes/'),

  /**
   * Get ballot results
   */
  getResults: (ballotId) =>
    new APIClient().get(`/ballots/ballots/${ballotId}/results/`),
};

/**
 * Chat API methods
 */
export const ChatAPI = {
  /**
   * Get all chat rooms
   */
  getRooms: () => new APIClient().get('/chat/rooms/'),

  /**
   * Get room by ID
   */
  getRoom: (id) => new APIClient().get(`/chat/rooms/${id}/`),

  /**
   * Get messages in room
   */
  getMessages: (roomId) =>
    new APIClient().get(`/chat/rooms/${roomId}/messages/`),

  /**
   * Create chat room (exec only)
   */
  createRoom: (name, description) =>
    new APIClient().post('/chat/rooms/', { name, description }),

  /**
   * Delete chat room (exec only)
   */
  deleteRoom: (id) => new APIClient().delete(`/chat/rooms/${id}/`),
};

/**
 * Resources API methods
 */
export const ResourcesAPI = {
  /**
   * Get all resources
   */
  getResources: () => new APIClient().get('/resources/resources/'),

  /**
   * Create resource (exec only)
   */
  createResource: (title, description, file) => {
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('file', file);

    return new APIClient().post('/resources/resources/', formData, {
      'Content-Type': 'multipart/form-data',
    });
  },

  /**
   * Get submissions
   */
  getSubmissions: () => new APIClient().get('/resources/submissions/'),

  /**
   * Create submission
   */
  createSubmission: (resourceId, file) => {
    const formData = new FormData();
    formData.append('resource_id', resourceId);
    formData.append('file', file);

    return new APIClient().post('/resources/submissions/', formData, {
      'Content-Type': 'multipart/form-data',
    });
  },
};

/**
 * Notifications API methods
 */
export const NotificationsAPI = {
  /**
   * Get user notifications
   */
  getNotifications: () =>
    new APIClient().get('/notifications/notifications/'),

  /**
   * Mark notification as read
   */
  markAsRead: (id) =>
    new APIClient().patch(`/notifications/notifications/${id}/`, {
      read: true,
    }),

  /**
   * Mark all as read
   */
  markAllAsRead: () =>
    new APIClient().post('/notifications/notifications/mark_all_as_read/', {}),

  /**
   * Delete notification
   */
  deleteNotification: (id) =>
    new APIClient().delete(`/notifications/notifications/${id}/`),

  /**
   * Subscribe to notification type
   */
  subscribe: (notificationType) =>
    new APIClient().post('/notifications/subscriptions/', {
      notification_type: notificationType,
    }),

  /**
   * Unsubscribe from notification type
   */
  unsubscribe: (notificationType) =>
    new APIClient().delete(
      `/notifications/subscriptions/${notificationType}/`
    ),
};

/**
 * Utility function for handling API errors
 */
export function handleAPIError(error) {
  if (error.response) {
    // Server responded with error status
    return {
      status: error.response.status,
      message: error.response.data?.detail || 'Server error',
      data: error.response.data,
    };
  } else if (error.request) {
    // Request made but no response
    return {
      status: 0,
      message: 'No response from server. Check your connection.',
    };
  } else {
    // Error in request setup
    return {
      status: 0,
      message: error.message,
    };
  }
}

export default new APIClient();
