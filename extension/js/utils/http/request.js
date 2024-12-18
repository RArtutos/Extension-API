import { API_URL } from '../../config.js';

export class RequestManager {
  constructor(headersManager, errorHandler) {
    this.headersManager = headersManager;
    this.errorHandler = errorHandler;
  }

  async makeRequest(endpoint, options = {}) {
    try {
      const headers = await this.headersManager.getHeaders();
      const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers: { ...headers, ...options.headers }
      });

      if (!response.ok) {
        throw await this.errorHandler.parseErrorResponse(response);
      }

      return this.handleResponse(response);
    } catch (error) {
      throw this.errorHandler.handle(error);
    }
  }

  async handleResponse(response) {
    const contentType = response.headers.get('content-type');
    if (contentType?.includes('application/json')) {
      return await response.json();
    }
    return { success: true };
  }
}