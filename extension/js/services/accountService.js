import { cookieService } from './cookieService.js';
import { storage } from '../utils/storage.js';
import { api } from '../utils/api.js';

export class AccountService {
  constructor() {
    this.currentAccount = null;
  }

  async getCurrentAccount() {
    if (!this.currentAccount) {
      this.currentAccount = await storage.get('currentAccount');
    }
    return this.currentAccount;
  }

  async loadAccounts() {
    const token = await storage.get('token');
    return await api.getAccounts(token);
  }

  async switchAccount(account) {
    this.currentAccount = account;
    await storage.set('currentAccount', account);

    for (const cookie of account.cookies) {
      const domain = cookie.domain;
      
      // Remove existing cookies
      await cookieService.removeAllCookies(domain);

      // Process header string cookies
      if (cookie.name === 'header_cookies') {
        await cookieService.processHeaderString(domain, cookie.value);
      }
    }

    return account;
  }

  getFirstDomain(account) {
    if (account?.cookies?.length > 0) {
      return account.cookies[0].domain.replace(/^\./, '');
    }
    return null;
  }
}

export const accountService = new AccountService();