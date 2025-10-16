import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 90000, // 90 seconds - allow for longer portfolio queries
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens here in future
    // config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    // Handle errors globally
    let message = 'An unexpected error occurred';

    if (error.response) {
      // Server responded with error status
      const data = error.response.data;
      
      // Handle different error response formats
      if (typeof data === 'string') {
        message = data;
      } else if (data?.detail) {
        // FastAPI validation error format
        if (typeof data.detail === 'string') {
          message = data.detail;
        } else if (Array.isArray(data.detail)) {
          // Pydantic validation errors
          message = data.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join(', ');
        } else {
          message = JSON.stringify(data.detail);
        }
      } else if (data?.message) {
        message = data.message;
      } else if (data?.error) {
        message = data.error;
      } else {
        // Fallback: stringify the entire error object
        message = JSON.stringify(data);
      }
    } else if (error.request) {
      // Request made but no response (timeout or network error)
      if (error.code === 'ECONNABORTED') {
        message = 'Request timeout. The server took too long to respond. Please try again.';
      } else {
        message = 'Cannot connect to server. Please check if the backend is running.';
      }
    } else {
      // Something else happened
      message = error.message || message;
    }

    console.error('API Error:', {
      message,
      status: error.response?.status,
      url: error.config?.url,
      method: error.config?.method,
      data: error.response?.data
    });

    return Promise.reject(new Error(message));
  }
);

export const apiService = {
  // Health check
  health: () => api.get('/health'),

  // Query endpoints
  query: (data) => api.post('/api/v1/query', data),
  clarify: (data) => api.post('/api/v1/query/clarify', data),

  // Session endpoints
  getSession: (sessionId) => api.get(`/api/v1/session/${sessionId}`),
  deleteSession: (sessionId) => api.delete(`/api/v1/session/${sessionId}`),

  // Portfolio endpoints
  getPortfolio: (clientId) => api.get(`/api/v1/clients/${clientId}/portfolio`),
};

export default api;
