import { API_URL } from '../../config/constants.js';
import { storage } from '../storage.js';
import { STORAGE_KEYS } from '../../config/constants.js';
import { ErrorHandler } from '../errors/ErrorHandler.js';

export class HttpClient {
  constructor(baseUrl = API_URL) {
    this.baseUrl = baseUrl;
  }

  async getHeaders() {
    const token = await storage.get(STORAGE_KEYS.TOKEN);
    return {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : ''
    };
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

      if (!response.ok) {
        const error = await ErrorHandler.parseResponseError(response);
        throw error;
      }

      if (response.status === 204) {
        return { success: true };
      }

      return await response.json();
    } catch (error) {
      const parsedError = ErrorHandler.parseError(error);
      console.error(`Request failed for ${endpoint}:`, parsedError.message);
      throw parsedError;
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