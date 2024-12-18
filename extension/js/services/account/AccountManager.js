import { storage } from '../../utils/storage.js';
import { SessionManager } from '../session/SessionManager.js';
import { cookieManager } from '../../utils/cookie/cookieManager.js';
import { analyticsService } from '../analyticsService.js';
import { AccountAPI } from './AccountAPI.js';

export class AccountManager {
  constructor() {
    this.api = new AccountAPI();
    this.sessionManager = new SessionManager();
    this.currentAccount = null;
  }

  async switchAccount(account) {
    try {
      // End current session if exists
      await this.sessionManager.cleanupCurrentSession();

      // Set new cookies
      await cookieManager.setAccountCookies(account);

      // Start new session
      const domain = this.getFirstDomain(account);
      if (!domain) {
        throw new Error('No valid domain found for account');
      }

      await this.sessionManager.startSession(account.id, domain);
      await analyticsService.trackAccountSwitch(this.currentAccount, account);
      
      // Update current account
      await storage.set('currentAccount', account);
      this.currentAccount = account;

      // Open domain in new tab
      await chrome.tabs.create({ url: `https://${domain}` });

      return true;
    } catch (error) {
      console.error('Failed to switch account:', error.message);
      throw error;
    }
  }

  getFirstDomain(account) {
    if (!account?.cookies?.length) return null;
    const domain = account.cookies[0].domain;
    return domain.startsWith('.') ? domain.substring(1) : domain;
  }
}