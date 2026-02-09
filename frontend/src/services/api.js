import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Violations API
export const violationAPI = {
  list: (params = {}) => api.get('/violations/', { params }),
  create: (data) => api.post('/violations/', data),
  retrieve: (id) => api.get(`/violations/${id}/`),
  update: (id, data) => api.patch(`/violations/${id}/`, data),
  delete: (id) => api.delete(`/violations/${id}/`),
  verify: (id) => api.post(`/violations/${id}/verify_violation/`),
  pending: (params = {}) => api.get('/violations/pending_review/', { params }),
  statistics: () => api.get('/violations/statistics/'),
};

// User Profile API
export const userAPI = {
  list: (params = {}) => api.get('/users/', { params }),
  retrieve: (id) => api.get(`/users/${id}/`),
  update: (id, data) => api.patch(`/users/${id}/`, data),
  addPoints: (id, points) => api.post(`/users/${id}/add_points/`, { points }),
  topContributors: () => api.get('/users/top_contributors/'),
  leaderboard: (params = {}) => api.get('/users/leaderboard/', { params }),
};

// Traffic Reports API
export const reportAPI = {
  list: (params = {}) => api.get('/reports/', { params }),
  create: (data) => api.post('/reports/', data),
  retrieve: (id) => api.get(`/reports/${id}/`),
  approve: (id, reward) => api.post(`/reports/${id}/approve_report/`, { reward }),
  reject: (id, reason) => api.post(`/reports/${id}/reject_report/`, { reason }),
  pending: (params = {}) => api.get('/reports/pending_reviews/', { params }),
};

// Fines API
export const fineAPI = {
  list: (params = {}) => api.get('/fines/', { params }),
  retrieve: (id) => api.get(`/fines/${id}/`),
  markPaid: (id, data) => api.post(`/fines/${id}/mark_as_paid/`, data),
  overdue: (params = {}) => api.get('/fines/overdue_fines/', { params }),
  revenueReport: () => api.get('/fines/revenue_report/'),
};

// Leaderboard API
export const leaderboardAPI = {
  list: (params = {}) => api.get('/leaderboards/', { params }),
  today: (params = {}) => api.get('/leaderboards/today/', { params }),
};

// Notifications API
export const notificationAPI = {
  list: (params = {}) => api.get('/notifications/', { params }),
  markAsRead: (id) => api.post(`/notifications/${id}/mark_as_read/`),
  markAllAsRead: () => api.post('/notifications/mark_all_as_read/'),
};

// Authentication API
export const authAPI = {
  login: (username, password) =>
    api.post('/auth/login/', { username, password }),
  register: (userData) =>
    api.post('/auth/register/', userData),
  logout: () => {
    localStorage.removeItem('access_token');
    return Promise.resolve();
  },
  currentUser: () => api.get('/auth/me/'),
};

export default api;
