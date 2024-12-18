import { httpClient } from '../../utils/http/HttpClient.js';

export class AccountAPI {
  async getAccounts() {
    return await httpClient.get('/api/accounts');
  }

  async getAccount(accountId) {
    return await httpClient.get(`/api/accounts/${accountId}`);
  }

  async getSessionInfo(accountId) {
    return await httpClient.get(`/api/accounts/${accountId}/session`);
  }
}