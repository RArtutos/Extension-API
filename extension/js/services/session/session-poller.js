import { SESSION_CONFIG } from '../../config/constants.js';

export class SessionPoller {
  constructor(updateCallback) {
    this.interval = null;
    this.updateCallback = updateCallback;
  }

  start() {
    if (this.interval) return;
    this.interval = setInterval(
      () => this.updateCallback(),
      SESSION_CONFIG.REFRESH_INTERVAL
    );
  }

  stop() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
  }
}