import { SESSION_CONFIG } from '../config/constants.js';
import { storage } from '../utils/storage.js';
import { httpClient } from '../utils/httpClient.js';
import { cookieManager } from '../utils/cookie/cookieManager.js';
import { analyticsService } from './analyticsService.js';

export class SessionManager {
  constructor() {
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

    try {
      const tabs = await chrome.tabs.query({});
      const hasOpenTabs = tabs.some((tab) => {
        try {
          if (!tab.url) return false;
          const domain = new URL(tab.url).hostname;
          return currentAccount.cookies.some((cookie) =>
            domain.endsWith(cookie.domain.replace(/^\./, ''))
          );
        } catch {
          return false;
        }
      });

      if (!hasOpenTabs) {
        await this.cleanupCurrentSession();
      }
    } catch (error) {
      console.error('Error handling tab close:', error);
    }
  }

  async startPolling() {
    if (this.pollInterval) return;

    this.pollInterval = setInterval(async () => {
      const currentAccount = await storage.get('currentAccount');
      if (currentAccount) {
        await this.updateSessionStatus(currentAccount.id);
      }
    }, SESSION_CONFIG.REFRESH_INTERVAL);
  }

  stopPolling() {
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
      this.pollInterval = null;
    }
  }

  async updateSessionStatus(accountId) {
    try {
      const sessionData = {
        active: true,
        timestamp: new Date().toISOString()
      };

      await httpClient.put(`/api/accounts/${accountId}/session`, sessionData);
      return true;
    } catch (error) {
      console.error('Error updating session status:', error);
      throw error;
    }
  }

  async cleanupCurrentSession() {
    try {
      const currentAccount = await storage.get('currentAccount');
      if (!currentAccount) return;

      await httpClient.post(`/api/accounts/${currentAccount.id}/session/end`);
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
    }
  }

  async startSession(accountId, domain) {
    try {
      // First check session limits
      const sessionInfo = await httpClient.get(`/api/accounts/${accountId}/session`);
      if (sessionInfo.active_sessions >= sessionInfo.max_concurrent_users) {
        throw new Error('Maximum concurrent users reached');
      }

      // Start new session
      const response = await httpClient.post(`/api/accounts/${accountId}/session/start`, {
        domain: domain
      });

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

  clearAllTimers() {
    this.activeTimers.forEach((timer) => {
      if (timer) clearTimeout(timer);
    });
    this.activeTimers.clear();
  }

  getAccountDomain(account) {
    if (!account?.cookies?.length) return '';
    const domain = account.cookies[0].domain;
    return domain.startsWith('.') ? domain.substring(1) : domain;
  }
}
