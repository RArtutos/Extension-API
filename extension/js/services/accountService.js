import { cookieService } from './cookieService.js';
import { storage } from '../utils/storage.js';
import { api } from '../utils/api.js';
import { STORAGE_KEYS } from '../config.js';

class AccountService {
  constructor() {
    this.currentAccount = null;
  }

  async getCurrentAccount() {
    if (!this.currentAccount) {
      this.currentAccount = await storage.get(STORAGE_KEYS.CURRENT_ACCOUNT);
    }
    return this.currentAccount;
  }

  async loadAccounts() {
    const token = await storage.get(STORAGE_KEYS.TOKEN);
    return await api.getAccounts(token);
  }

  async switchAccount(account) {
    try {
      // Get session info first
      const sessionInfo = await api.getSessionInfo(account.id);
      if (sessionInfo.active_sessions >= sessionInfo.max_concurrent_users) {
        throw new Error(`Maximum concurrent users (${sessionInfo.max_concurrent_users}) reached`);
      }

      // Remove current account cookies
      const currentAccount = await this.getCurrentAccount();
      if (currentAccount) {
        for (const cookie of currentAccount.cookies) {
          await cookieService.removeAllCookies(cookie.domain);
        }
      }

      // Set new account cookies
      for (const cookie of account.cookies) {
        if (cookie.name === 'header_cookies') {
          await cookieService.processHeaderString(cookie.domain, cookie.value);
        }
      }

      // Update storage
      this.currentAccount = account;
      await storage.set(STORAGE_KEYS.CURRENT_ACCOUNT, account);

      return account;
    } catch (error) {
      console.error('Error switching account:', error);
      throw error;
    }
  }

  getFirstDomain(account) {
    if (account?.cookies?.length > 0) {
      return account.cookies[0].domain.replace(/^\./, '');
    }
    return null;
  }
}

export const accountService = new AccountService();