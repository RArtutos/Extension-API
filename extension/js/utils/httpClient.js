import { API_URL } from '../config/constants.js';
import { storage } from './storage.js';
import { STORAGE_KEYS } from '../config/constants.js';
import { RequestBuilder } from './http/requestBuilder.js';
import { ResponseHandler } from './http/responseHandler.js';

class HttpClient {
  constructor() {
    this.baseUrl = API_URL;
  }

  async getHeaders() {
    const token = await storage.get(STORAGE_KEYS.TOKEN);
    return RequestBuilder.createHeaders(token);
  }

  async get(endpoint) {
    try {
      const headers = await this.getHeaders();
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'GET',
        headers
      });

      return await ResponseHandler.handle(response);
    } catch (error) {
      console.error(`GET request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  async post(endpoint, data, options = {}) {
    try {
      const headers = await this.getHeaders();
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        headers: options.formData ? {
          'Content-Type': 'application/x-www-form-urlencoded'
        } : headers,
        body: options.formData ? 
          RequestBuilder.createFormData(data) : 
          JSON.stringify(data)
      });

      return await ResponseHandler.handle(response);
    } catch (error) {
      console.error(`POST request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  async put(endpoint, data) {
    try {
      const headers = await this.getHeaders();
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(data)
      });

      return await ResponseHandler.handle(response);
    } catch (error) {
      console.error(`PUT request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  async delete(endpoint) {
    try {
      const headers = await this.getHeaders();
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'DELETE',
        headers
      });

      return await ResponseHandler.handle(response);
    } catch (error) {
      console.error(`DELETE request failed for ${endpoint}:`, error);
      throw error;
    }
  }
}

export const httpClient = new HttpClient();