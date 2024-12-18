import { API_URL } from '../../config/constants.js';

export class AuthApi {
  static async login(email, password) {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData
    });

    if (!response.ok) {
      throw new Error('Authentication failed');
    }

    return response.json();
  }

  static async validateToken(token) {
    const response = await fetch(`${API_URL}/api/auth/validate`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Token validation failed');
    }

    return response.json();
  }
}