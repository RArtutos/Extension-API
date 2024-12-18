import { httpClient } from '../utils/httpClient.js';
import { storage } from '../utils/storage.js';
import { SESSION_CONFIG } from '../config/constants.js';
import { analyticsService } from './analyticsService.js';

class SessionService {
  constructor() {
    this.activeTimers = new Map();
  }

  async startSession(accountId, domain) {
    try {
      // Check session limits first
      const sessionInfo = await this.getSessionInfo(accountId);
      if (sessionInfo.active_sessions >= sessionInfo.max_concurrent_users) {
        throw new Error(`Maximum concurrent users (${sessionInfo.max_concurrent_users}) reached`);
      }

      // Update session activity
      const response = await httpClient.put(`/api/accounts/${accountId}/session`, {
        domain: domain,
        active: true
      });

      if (response.success) {
        await analyticsService.trackSessionStart(accountId, domain);
        this.startInactivityTimer(domain, accountId);
      }

      return response.success;
    } catch (error) {
      console.error('Error starting session:', error);
      throw error;
    }
  }

  async updateSession(accountId, domain) {
    try {
      const response = await httpClient.put(`/api/accounts/${accountId}/session`, {
        domain: domain,
        active: true
      });

      if (response.success) {
        await analyticsService.trackPageView(domain);
        this.startInactivityTimer(domain, accountId);
      }

      return response.success;
    } catch (error) {
      console.error('Error updating session:', error);
      return false;
    }
  }

  async endSession(accountId, domain) {
    try {
      const response = await httpClient.put(`/api/accounts/${accountId}/session`, {
        active: false
      });
      
      if (response.success) {
        await analyticsService.trackSessionEnd(accountId, domain);
        this.clearInactivityTimer(domain);
      }
      return response.success;
    } catch (error) {
      console.error('Error ending session:', error);
      return false;
    }
  }

  async getSessionInfo(accountId) {
    try {
      return await httpClient.get(`/api/accounts/${accountId}/session`);
    } catch (error) {
      console.error('Error getting session info:', error);
      throw error;
    }
  }

  startInactivityTimer(domain, accountId) {
    this.clearInactivityTimer(domain);

    const timer = setTimeout(
      () => this.handleInactivity(domain, accountId),
      SESSION_CONFIG.INACTIVITY_TIMEOUT
    );

    this.activeTimers.set(domain, timer);
  }

  clearInactivityTimer(domain) {
    if (this.activeTimers.has(domain)) {
      clearTimeout(this.activeTimers.get(domain));
      this.activeTimers.delete(domain);
    }
  }

  async handleInactivity(domain, accountId) {
    this.clearInactivityTimer(domain);
    await this.endSession(accountId, domain);
  }
}

export const sessionService = new SessionService();