import { storage } from '../utils/storage.js';
import { httpClient } from '../utils/httpClient.js';
import { cookieManager } from '../utils/cookie/cookieManager.js';
import { analyticsService } from './analyticsService.js';
import { SessionPoller } from './session/session-poller.js';
import { TabMonitor } from './session/tab-monitor.js';
import { getAccountDomain } from './session/domain-utils.js';

export class SessionManager {
  constructor() {
    this.activeTimers = new Map();
    this.poller = new SessionPoller(() => this.updateCurrentSession());
    this.tabMonitor = new TabMonitor(() => this.cleanupCurrentSession());
  }

  async startSession(accountId, domain) {
    try {
      const sessionInfo = await httpClient.get(`/api/accounts/${accountId}/session`);
      if (sessionInfo.active_sessions >= sessionInfo.max_concurrent_users) {
        throw new Error('Maximum concurrent users reached');
      }

      const response = await httpClient.post(`/api/accounts/${accountId}/session/start`, {
        domain: domain
      });

      if (response.success) {
        await analyticsService.trackSessionStart(accountId, domain);
        this.poller.start();
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error starting session:', error);
      throw error;
    }
  }

  async updateCurrentSession() {
    try {
      const currentAccount = await storage.get('currentAccount');
      if (!currentAccount) return;

      const currentDomain = window.location.hostname;
      await httpClient.put(`/api/accounts/${currentAccount.id}/session`, {
        active: true,
        domain: currentDomain,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      console.error('Error updating session:', error);
    }
  }

  async cleanupCurrentSession() {
    try {
      const currentAccount = await storage.get('currentAccount');
      if (!currentAccount) return;

      await httpClient.post(`/api/accounts/${currentAccount.id}/session/end`);
      await analyticsService.trackSessionEnd(
        currentAccount.id, 
        getAccountDomain(currentAccount)
      );
      
      await cookieManager.removeAccountCookies(currentAccount);
      await storage.remove('currentAccount');
      
      this.poller.stop();
      this.clearTimers();
    } catch (error) {
      console.error('Error cleaning up session:', error);
      throw error;
    }
  }

  clearTimers() {
    this.activeTimers.forEach(timer => clearTimeout(timer));
    this.activeTimers.clear();
  }
}