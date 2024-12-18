import { API_URL } from '../config/constants.js';
import { authService } from '../services/authService.js';

class HttpClient {
  async getHeaders() {
    const token = await authService.getToken();
    return {
      'Authorization': token ? `Bearer ${token}` : '',
      'Content-Type': 'application/json'
    };
  }

  async get(endpoint) {
    try {
      const headers = await this.getHeaders();
      const response = await fetch(`${API_URL}${endpoint}`, { headers });
      
      if (!response.ok) {
        if (response.status === 401) {
          await authService.logout();
        }
        throw new Error(await this.handleErrorResponse(response));
      }

      return await response.json();
    } catch (error) {
      console.error('GET request failed:', error);
      throw error;
    }
  }

  async put(endpoint, data) {
    try {
      const headers = await this.getHeaders();
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(await this.handleErrorResponse(response));
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      }
      return { success: true };
    } catch (error) {
      console.error('PUT request failed:', error);
      throw error;
    }
  }

  async post(endpoint, data) {
    try {
      const headers = await this.getHeaders();
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(await this.handleErrorResponse(response));
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      }
      return { success: true };
    } catch (error) {
      console.error('POST request failed:', error);
      throw error;
    }
  }

  async handleErrorResponse(response) {
    try {
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const errorData = await response.json();
        return errorData.detail || errorData.message || 'Request failed';
      }
      return 'Request failed';
    } catch {
      return 'Request failed';
    }
  }
}

export const httpClient = new HttpClient();