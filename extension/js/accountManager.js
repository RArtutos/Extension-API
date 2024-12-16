import { api } from './utils/api.js';
import { storage } from './utils/storage.js';
import { ui } from './utils/ui.js';
import { cookieManager } from './utils/cookieManager.js';

class AccountManager {
  constructor() {
    this.currentAccount = null;
    this.proxyEnabled = false;
  }

  async init() {
    const token = await storage.get('token');
    if (token) {
      ui.showAccountManager();
      await this.loadAccounts();
    } else {
      ui.showLoginForm();
    }
  }

  async login(email, password) {
    try {
      const response = await api.login(email, password);
      if (response.access_token) {
        await storage.set('token', response.access_token);
        ui.showAccountManager();
        await this.loadAccounts();
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      ui.showError('Login failed: ' + (error.message || 'Unknown error'));
    }
  }

  async logout() {
    await storage.remove(['token', 'currentAccount']);
    this.currentAccount = null;
    ui.showLoginForm();
  }

  async loadAccounts() {
    try {
      const accounts = await api.getAccounts();
      this.currentAccount = await storage.get('currentAccount');
      ui.updateAccountsList(accounts, this.currentAccount);
    } catch (error) {
      ui.showError('Failed to load accounts: ' + error.message);
    }
  }

  async switchAccount(account) {
    try {
      // Get session info
      const sessionInfo = await api.getSessionInfo(account.id);
      if (sessionInfo.active_sessions >= sessionInfo.max_concurrent_users) {
        throw new Error(`Maximum concurrent users (${sessionInfo.max_concurrent_users}) reached`);
      }

      // Remove current account cookies
      if (this.currentAccount) {
        await cookieManager.removeAccountCookies(this.currentAccount);
      }

      // Set new account cookies
      await cookieManager.setAccountCookies(account);
      
      // Update storage and state
      this.currentAccount = account;
      await storage.set('currentAccount', account);

      // Update UI
      const accounts = await api.getAccounts();
      ui.updateAccountsList(accounts, account);
      ui.showSuccess('Account switched successfully');

      // Open first domain if available
      const firstDomain = this.getFirstDomain(account);
      if (firstDomain) {
        chrome.tabs.create({ url: `https://${firstDomain}` });
      }
    } catch (error) {
      ui.showError('Error switching account: ' + error.message);
    }
  }

  getFirstDomain(account) {
    if (account.cookies && account.cookies.length > 0) {
      const domain = account.cookies[0].domain;
      return domain.startsWith('.') ? domain.substring(1) : domain;
    }
    return null;
  }

  setProxyEnabled(enabled) {
    this.proxyEnabled = enabled;
    if (this.currentAccount) {
      this.updateProxy();
    }
  }

  async updateProxy() {
    // Implement proxy update logic here
    console.log('Updating proxy settings...');
  }

  async showStats() {
    // Implement stats display logic here
    console.log('Showing stats...');
  }
}

export const accountManager = new AccountManager();