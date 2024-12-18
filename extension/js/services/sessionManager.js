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

  async startSession(accountId, domain) {
    try {
      // First check session limits
      const sessionInfo = await httpClient.get(`/api/accounts/${accountId}/session`);
      if (sessionInfo.active_sessions >= sessionInfo.max_concurrent_users) {
        throw new Error('Maximum concurrent users reached');
      }

      // Start new session - Asegurarse de enviar el dominio en el formato correcto
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
      console.error('Error starting session:', error.message);
      throw new Error(error.response?.data?.detail || 'Failed to start session');
    }
  }

  async updateSessionStatus(accountId) {
    try {
      const sessionData = {
        active: true,
        domain: window.location.hostname, // Incluir el dominio actual
        timestamp: new Date().toISOString()
      };

      await httpClient.put(`/api/accounts/${accountId}/session`, sessionData);
      return true;
    } catch (error) {
      console.error('Error updating session status:', error.message);
      throw new Error(error.response?.data?.detail || 'Failed to update session');
    }
  }

  // ... resto del código sin cambios ...
}