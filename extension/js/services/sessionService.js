import { storage } from '../utils/storage.js';
import { httpClient } from '../utils/httpClient.js';
import { SESSION_CONFIG } from '../config/constants.js';

class SessionService {
  constructor() {
    this.activeTimers = new Map();
  }

  async startSession(accountId, domain) {
    try {
      const response = await httpClient.post('/api/sessions', {
        account_id: accountId,
        domain: domain
      });
      return response.success;
    } catch (error) {
      console.error('Error starting session:', error);
      return false;
    }
  }

  async updateSession(accountId, domain) {
    try {
      const response = await httpClient.put(`/api/sessions/${accountId}`, {
        domain: domain
      });
      return response.success;
    } catch (error) {
      console.error('Error updating session:', error);
      return false;
    }
  }

  async endSession(accountId) {
    try {
      const response = await httpClient.delete(`/api/sessions/${accountId}`);
      return response.success;
    } catch (error) {
      console.error('Error ending session:', error);
      return false;
    }
  }

  startInactivityTimer(domain, accountId) {
    if (this.activeTimers.has(domain)) {
      clearTimeout(this.activeTimers.get(domain));
    }

    const timer = setTimeout(
      () => this.handleInactivity(domain, accountId),
      SESSION_CONFIG.INACTIVITY_TIMEOUT
    );

    this.activeTimers.set(domain, timer);
  }

  async handleInactivity(domain, accountId) {
    this.activeTimers.delete(domain);
    await this.endSession(accountId);
  }
}

export const sessionService = new SessionService();