class Api {
  constructor() {
    this.baseUrl = 'http://84.46.249.121:8000/api';
  }

  async login(email, password) {
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const response = await fetch(`${this.baseUrl}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error('Invalid credentials');
      }

      return await response.json();
    } catch (error) {
      throw new Error(error.message || 'Login failed');
    }
  }

  async getAccounts() {
    try {
      const token = await chrome.storage.local.get('token');
      if (!token.token) throw new Error('No authentication token');

      const response = await fetch(`${this.baseUrl}/accounts`, {
        headers: {
          'Authorization': `Bearer ${token.token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch accounts');
      }

      return await response.json();
    } catch (error) {
      throw new Error(error.message || 'Failed to load accounts');
    }
  }

  async getSessionInfo(accountId) {
    try {
      const token = await chrome.storage.local.get('token');
      if (!token.token) throw new Error('No authentication token');

      const response = await fetch(`${this.baseUrl}/accounts/${accountId}/session`, {
        headers: {
          'Authorization': `Bearer ${token.token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch session info');
      }

      return await response.json();
    } catch (error) {
      throw new Error(error.message || 'Failed to get session info');
    }
  }
}

export const api = new Api();