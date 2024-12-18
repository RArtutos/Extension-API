import { SESSION_CONFIG } from '../../config/constants.js';
import { storage } from '../../utils/storage.js';
import { cookieManager } from '../../utils/cookie/cookieManager.js';
import { analyticsService } from '../analytics/analyticsService.js';
import { SessionAPI } from './sessionAPI.js';
import { TabManager } from './tabManager.js';
import { SessionValidator } from './sessionValidator.js';

export class SessionManager {
  constructor() {
    this.api = new SessionAPI();
    this.tabManager = new TabManager();
    this.validator = new SessionValidator();
    this.activeTimers = new Map();
    this.pollInterval = null;
    this.initializeSessionCleanup();
  }

  initializeSessionCleanup() {
    chrome.tabs.onRemoved.addListener(async (tabId) => {
      await this.handleTabClose();
    });
  }

  async handleTabClose() {
    const currentAccount = await storage.get('currentAccount');
    if (!currentAccount) return;

    const hasOpenTabs = await this.tabManager.hasOpenTabsForAccount(currentAccount);
    if (!hasOpenTabs) {
      await this.cleanupCurrentSession();
    }
  }

  async startSession(accountId, domain) {
    try {
      await this.validator.validateSessionLimit(accountId);
      const response = await this.api.startSession(accountId, domain);
      
      if (response.success) {
        await analyticsService.trackSessionStart(accountId, domain);
        this.startPolling();
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error starting session:', error);
      throw error;
    }
  }

  async cleanupCurrentSession() {
    try {
      const currentAccount = await storage.get('currentAccount');
      if (!currentAccount) return;

      await this.api.endSession(currentAccount.id);
      await analyticsService.trackSessionEnd(
        currentAccount.id,
        this.getAccountDomain(currentAccount)
      );

      await cookieManager.removeAccountCookies(currentAccount);
      await storage.remove('currentAccount');
      this.stopPolling();
      this.clearAllTimers();
    } catch (error) {
      console.error('Error cleaning up session:', error);
      throw error;
    }
  }

  private getAccountDomain(account) {
    if (!account?.cookies?.length) return '';
    const domain = account.cookies[0].domain;
    return domain.startsWith('.') ? domain.substring(1) : domain;
  }

  private startPolling() {
    if (this.pollInterval) return;
    this.pollInterval = setInterval(async () => {
      const currentAccount = await storage.get('currentAccount');
      if (currentAccount) {
        await this.api.updateSessionStatus(currentAccount.id);
      }
    }, SESSION_CONFIG.REFRESH_INTERVAL);
  }

  private stopPolling() {
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
      this.pollInterval = null;
    }
  }

  private clearAllTimers() {
    this.activeTimers.forEach(timer => clearTimeout(timer));
    this.activeTimers.clear();
  }
}