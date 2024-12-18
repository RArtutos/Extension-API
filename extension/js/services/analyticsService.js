import { httpClient } from '../utils/httpClient.js';
import { storage } from '../utils/storage.js';
import { ANALYTICS_CONFIG } from '../config/constants.js';

class AnalyticsService {
  constructor() {
    this.pendingEvents = [];
    this.timers = new Map();
    this.initializeTracking();
  }

  async initializeTracking() {
    setInterval(() => this.flushEvents(), ANALYTICS_CONFIG.TRACKING_INTERVAL);
  }

  resetTimer(domain) {
    if (this.timers.has(domain)) {
      clearTimeout(this.timers.get(domain));
    }
    
    const timer = setTimeout(() => {
      this.trackPageView(domain);
    }, ANALYTICS_CONFIG.TRACKING_INTERVAL);
    
    this.timers.set(domain, timer);
  }

  async trackEvent(eventData) {
    const userData = await storage.get('userData');
    if (!userData?.email) return;

    const event = {
      ...eventData,
      user_id: userData.email,
      timestamp: new Date().toISOString()
    };

    await httpClient.post(`/api/analytics/user/${userData.email}/events`, {
      event: event
    });
  }

  async trackPageView(domain) {
    await this.trackEvent({
      type: 'pageview',
      domain,
      action: 'view'
    });
  }

  async trackAccountSwitch(fromAccount, toAccount) {
    await this.trackEvent({
      type: 'account_switch',
      from: fromAccount?.id,
      to: toAccount.id,
      action: 'switch'
    });
  }

  async trackSessionStart(accountId, domain) {
    await this.trackEvent({
      type: 'session',
      account_id: accountId,
      domain,
      action: 'start'
    });
  }

  async trackSessionEnd(accountId, domain) {
    await this.trackEvent({
      type: 'session',
      account_id: accountId,
      domain,
      action: 'end'
    });
  }
}

export const analyticsService = new AnalyticsService();