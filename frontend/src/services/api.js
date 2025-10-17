/**
 * API service for communicating with the backend.
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Products API
export const productsApi = {
  getAll: (params = {}) => apiClient.get('/products/', { params }),
  getById: (id) => apiClient.get(`/products/${id}`),
  getCategories: () => apiClient.get('/products/categories/list'),
  create: (data) => apiClient.post('/products/', data),
};

// Users API
export const usersApi = {
  getAll: (params = {}) => apiClient.get('/users/', { params }),
  getById: (id) => apiClient.get(`/users/${id}`),
  create: (data) => apiClient.post('/users/', data),
};

// Interactions API
export const interactionsApi = {
  create: (data) => apiClient.post('/interactions/', data),
  getByUser: (userId, params = {}) => 
    apiClient.get(`/interactions/user/${userId}`, { params }),
  getByProduct: (productId, params = {}) => 
    apiClient.get(`/interactions/product/${productId}`, { params }),
};

// Recommendations API
export const recommendationsApi = {
  generate: (data) => apiClient.post('/recommendations/generate', data),
  getByUser: (userId, params = {}) => 
    apiClient.get(`/recommendations/${userId}`, { params }),
  getUserInsights: (userId) => 
    apiClient.get(`/recommendations/insights/${userId}`),
};

export default apiClient;