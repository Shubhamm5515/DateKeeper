import axios from 'axios';
import API_URL from '../config/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add authentication token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 errors (unauthorized)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// OCR Services
export const extractExpiryDate = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const token = localStorage.getItem('token');
  const response = await axios.post(
    `${API_URL}/api/ocr/extract-expiry`,
    formData,
    {
      headers: { 
        'Content-Type': 'multipart/form-data',
        'Authorization': token ? `Bearer ${token}` : ''
      }
    }
  );
  
  return response.data;
};

export const checkOCRHealth = async () => {
  const response = await api.get('/api/ocr/health');
  return response.data;
};

// Document Services (now use authenticated API)
export const createDocument = async (documentData) => {
  const response = await api.post('/api/documents/', documentData);
  return response.data;
};

export const getDocuments = async () => {
  const response = await api.get('/api/documents/');
  return response.data;
};

export const getDocument = async (documentId) => {
  const response = await api.get(`/api/documents/${documentId}`);
  return response.data;
};

export const updateDocument = async (documentId, documentData) => {
  const response = await api.put(`/api/documents/${documentId}`, documentData);
  return response.data;
};

export const deleteDocument = async (documentId) => {
  const response = await api.delete(`/api/documents/${documentId}`);
  return response.data;
};

export const getDocumentStats = async () => {
  const response = await api.get('/api/documents/stats/summary');
  return response.data;
};

export default api;
