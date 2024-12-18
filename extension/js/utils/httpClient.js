import { API_URL } from '../config/constants.js';
import { authService } from '../services/authService.js';
import { ErrorHandler } from './errorHandler.js';

class HttpClient {
  constructor() {
    this.errorHandler = new ErrorHandler();
  }

  async getHeaders() {
    const token = await authService.getToken();
    return {
      'Authorization': token ? `Bearer ${token}` : '',
      'Content-Type': 'application/json'
    };
  }

  async get(endpoint) {
    try {
      const response = await this.makeRequest(endpoint);
      return await this.handleResponse(response);
    } catch (error) {
      throw this.errorHandler.handle(error);
    }
  }

  async post(endpoint, data) {
    try {
      const response = await this.makeRequest(endpoint, {
        method: 'POST',
        body: JSON.stringify(data)
      });
      return await this.handleResponse(response);
    } catch (error) {
      throw this.errorHandler.handle(error);
    }
  }

  async put(endpoint, data) {
    try {
      const response = await this.makeRequest(endpoint, {
        method: 'PUT',
        body: JSON.stringify(data)
      });
      return await this.handleResponse(response);
    } catch (error) {
      throw this.errorHandler.handle(error);
    }
  }

  private async makeRequest(endpoint, options = {}) {
    const headers = await this.getHeaders();
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: { ...headers, ...options.headers }
    });

    if (!response.ok) {
      const error = await this.errorHandler.parseErrorResponse(response);
      throw error;
    }

    return response;
  }

  private async handleResponse(response) {
    const contentType = response.headers.get('content-type');
    if (contentType?.includes('application/json')) {
      return await response.json();
    }
    return { success: true };
  }
}

export const httpClient = new HttpClient();