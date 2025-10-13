import axios from 'axios';
import { getToken, setToken, removeTokens, getRefreshToken } from '../utils/auth';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = getRefreshToken();
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {}, {
          headers: {
            Authorization: `Bearer ${refreshToken}`,
          },
        });

        const { access_token } = response.data;
        setToken(access_token);

        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        removeTokens();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

// Chatbot APIs
export const chatbotAPI = {
  sendMessage: (message) => api.post('/chatbot/chat', { message }),
  getHistory: (skip = 0, limit = 50) => api.get(`/chatbot/history?skip=${skip}&limit=${limit}`),
  deleteHistory: () => api.delete('/chatbot/history'),
  getSuggestions: () => api.get('/chatbot/suggestions'),
};

// Career APIs
export const careerAPI = {
  getAll: (skip = 0, limit = 50) => api.get(`/careers?skip=${skip}&limit=${limit}`),
  getById: (id) => api.get(`/careers/${id}`),
  search: (query) => api.get(`/careers/search?q=${query}`),
  recommend: (interests) => api.post('/careers/recommend', { interests }),
};

// User APIs
export const userAPI = {
  getProfile: () => api.get('/user/profile'),
  updateProfile: (data) => api.put('/user/profile', data),
  getTestQuestions: (type = 'interest') => api.get(`/user/test/questions?type=${type}`),
  submitTest: (data) => api.post('/user/test/submit', data),
  getTestResults: (skip = 0, limit = 20) => api.get(`/user/test/results?skip=${skip}&limit=${limit}`),
  getLatestTestResult: (type) => api.get(`/user/test/results/latest${type ? `?type=${type}` : ''}`),
};

// Admin APIs
export const adminAPI = {
  getUsers: (skip = 0, limit = 50) => api.get(`/admin/users?skip=${skip}&limit=${limit}`),
  getUser: (userId) => api.get(`/admin/users/${userId}`),
  deactivateUser: (userId) => api.post(`/admin/users/${userId}/deactivate`),
  getStats: () => api.get('/admin/stats'),
  getRecentConversations: (limit = 100) => api.get(`/admin/conversations/recent?limit=${limit}`),
};

export default api;
