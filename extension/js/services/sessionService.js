import { httpClient } from '../utils/httpClient.js';

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
      throw error;
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
      throw error;
    }
  }

  async endSession(accountId) {
    try {
      const response = await httpClient.delete(`/api/sessions/${accountId}`);
      return response.success;
    } catch (error) {
      console.error('Error ending session:', error);
      throw error;
    }
  }
}

export const sessionService = new SessionService();