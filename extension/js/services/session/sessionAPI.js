import { httpClient } from '../../utils/httpClient.js';

export class SessionAPI {
  async startSession(accountId, domain) {
    try {
      return await httpClient.post(`/api/accounts/${accountId}/session/start`, { domain });
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async endSession(accountId) {
    try {
      return await httpClient.post(`/api/accounts/${accountId}/session/end`);
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async updateSessionStatus(accountId) {
    try {
      return await httpClient.put(`/api/accounts/${accountId}/session`, {
        active: true,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async getSessionInfo(accountId) {
    try {
      return await httpClient.get(`/api/accounts/${accountId}/session`);
    } catch (error) {
      throw this.handleError(error);
    }
  }

  private handleError(error) {
    if (error.response?.data?.detail) {
      return new Error(error.response.data.detail);
    }
    return error;
  }
}