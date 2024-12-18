import { httpClient } from '../../utils/http/HttpClient.js';

export class SessionAPI {
  async getSessionInfo(accountId) {
    return await httpClient.get(`/api/accounts/${accountId}/session`);
  }

  async startSession(accountId, domain) {
    return await httpClient.post(`/api/accounts/${accountId}/session/start`, { domain });
  }

  async updateSession(accountId, sessionData) {
    return await httpClient.put(`/api/accounts/${accountId}/session`, sessionData);
  }

  async endSession(accountId) {
    return await httpClient.post(`/api/accounts/${accountId}/session/end`);
  }
}