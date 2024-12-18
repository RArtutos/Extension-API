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
      await authService.logout();
      throw new Error('authentication_required');
    }

    if (!response.ok) {
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Request failed');
      }
      throw new Error(`Request failed with status ${response.status}`);
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
      console.error(`Request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // ... resto del código sin cambios ...
}

export const httpClient = new HttpClient();