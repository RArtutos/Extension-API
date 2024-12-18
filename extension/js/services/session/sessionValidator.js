import { SessionAPI } from './sessionAPI.js';

export class SessionValidator {
  constructor() {
    this.api = new SessionAPI();
  }

  async validateSessionLimit(accountId) {
    const sessionInfo = await this.api.getSessionInfo(accountId);
    if (sessionInfo.active_sessions >= sessionInfo.max_concurrent_users) {
      throw new Error('Maximum concurrent users reached');
    }
    return true;
  }
}