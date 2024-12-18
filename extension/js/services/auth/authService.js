import { storage } from '../../utils/storage.js';
import { STORAGE_KEYS } from '../../config/constants.js';
import { AuthApi } from './authApi.js';

class AuthService {
  async login(email, password) {
    const response = await AuthApi.login(email, password);
    
    if (response.access_token) {
      await storage.set(STORAGE_KEYS.TOKEN, response.access_token);
      await storage.set(STORAGE_KEYS.USER_DATA, {
        email,
        is_admin: response.is_admin || false
      });
      return response;
    }
    
    throw new Error('Invalid response from server');
  }

  async logout() {
    await storage.remove([
      STORAGE_KEYS.TOKEN,
      STORAGE_KEYS.CURRENT_ACCOUNT,
      STORAGE_KEYS.USER_DATA
    ]);
  }

  async isAuthenticated() {
    const token = await storage.get(STORAGE_KEYS.TOKEN);
    if (!token) return false;

    try {
      await AuthApi.validateToken(token);
      return true;
    } catch {
      await this.logout();
      return false;
    }
  }
}

export const authService = new AuthService();