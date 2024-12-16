import { API_URL } from '../config.js';

class Api {
  async login(email, password) {
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
    });
    
    if (!response.ok) {
      throw new Error('Invalid credentials');
    }
    
    return response.json();
  }

  async getAccounts(token) {
    const response = await fetch(`${API_URL}/api/accounts`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch accounts');
    }
    
    return response.json();
  }

  async getSessionInfo(accountId) {
    const token = await chrome.storage.local.get('token');
    if (!token.token) {
      throw new Error('No authentication token');
    }

    const response = await fetch(`${API_URL}/api/accounts/${accountId}/session`, {
      headers: {
        'Authorization': `Bearer ${token.token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch session info');
    }

    return response.json();
  }
}

export const api = new Api();