import { API_URL, STORAGE_KEYS, UI_CONFIG } from './config.js';
import { storage } from './utils/storage.js';
import { ui } from './utils/ui.js';
import { accountManager } from './accountManager.js';
import { cookieService } from './services/cookieService.js';
import { authService } from './services/authService.js';
import { httpClient } from './utils/httpClient.js';

class PopupManager {
  constructor() {
    this.initialized = false;
    this.refreshInterval = null;
  }

  async init() {
    if (this.initialized) return;
    
    this.attachEventListeners();
    await this.checkAuthState();
    this.initialized = true;
  }

  attachEventListeners() {
    document.getElementById('login-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      await this.handleLogin();
    });
    
    document.getElementById('logout-btn')?.addEventListener('click', () => this.handleLogout());
    document.getElementById('close-btn')?.addEventListener('click', () => window.close());
  }

  async checkAuthState() {
    try {
      const isAuthenticated = await authService.isAuthenticated();
      if (isAuthenticated) {
        await this.showAccountManager();
      } else {
        ui.showLoginForm();
      }
    } catch (error) {
      console.error('Error checking auth state:', error);
      ui.showLoginForm();
    }
  }

  async handleLogin() {
    const email = document.getElementById('email')?.value;
    const password = document.getElementById('password')?.value;

    if (!email || !password) {
      ui.showError('Please enter both email and password');
      return;
    }

    try {
      await authService.login(email, password);
      await this.showAccountManager();
      ui.showSuccess('Login successful');
    } catch (error) {
      console.error('Login failed:', error);
      ui.showError('Login failed. Please check your credentials and try again.');
    }
  }

  async handleLogout() {
    try {
      const currentAccount = await storage.get(STORAGE_KEYS.CURRENT_ACCOUNT);
      if (currentAccount) {
        await cookieService.removeAllCookies(currentAccount.domain);
      }

      await authService.logout();
      
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval);
        this.refreshInterval = null;
      }

      ui.showLoginForm();
      ui.showSuccess('Logged out successfully');
    } catch (error) {
      console.error('Logout failed:', error);
      ui.showError('Error during logout');
    }
  }

  async showAccountManager() {
    try {
      ui.showAccountManager();
      await this.loadAccounts();
      
      if (UI_CONFIG.REFRESH_INTERVAL) {
        this.refreshInterval = setInterval(() => this.loadAccounts(), UI_CONFIG.REFRESH_INTERVAL);
      }
    } catch (error) {
      console.error('Error showing account manager:', error);
      ui.showError('Error loading account manager');
    }
  }

  async loadAccounts() {
    try {
      const accounts = await httpClient.get('/api/accounts/');
      const currentAccount = await storage.get(STORAGE_KEYS.CURRENT_ACCOUNT);
      ui.updateAccountsList(accounts, currentAccount);
    } catch (error) {
      console.error('Failed to load accounts:', error);
      if (error.message === 'authentication_required') {
        await this.handleLogout();
      } else {
        ui.showError('Failed to load accounts. Please try again.');
      }
    }
  }
}

// Initialize popup
const popupManager = new PopupManager();
document.addEventListener('DOMContentLoaded', () => popupManager.init());