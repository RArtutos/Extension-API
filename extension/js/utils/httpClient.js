import { API_URL } from '../config/constants.js';
import { storage } from './storage.js';
import { STORAGE_KEYS } from '../config/constants.js';
import { authService } from '../services/authService.js';

class HttpClient {
  constructor() {
    this.baseUrl = API_URL;
  }

  async getHeaders() {
    const token = await storage.get(STORAGE_KEYS.TOKEN);
    return {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : ''
    };
  }

  async handleResponse(response) {
    if (response.status === 401) {
      // Token expired or invalid
      await authService.logout();
      throw new Error('authentication_required');
    }

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Request failed');
    }

    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    }
    
    return { success: true };
  }

  async request(endpoint, options = {}) {
    try {
      const headers = await this.getHeaders();
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          ...headers,
          ...options.headers
        }
      });

      return await this.handleResponse(response);
    } catch (error) {
      if (error.message === 'authentication_required') {
        throw error;
      }
      console.error('Request failed:', error.message);
      throw new Error(error.message || 'Request failed');
    }
  }

  async get(endpoint) {
    return this.request(endpoint);
  }

  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  async delete(endpoint) {
    return this.request(endpoint, {
      method: 'DELETE'
    });
  }
}

export const httpClient = new HttpClient();