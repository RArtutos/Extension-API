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
    this.pendingEvents.push({
      ...eventData,
      timestamp: new Date().toISOString()
    });

    if (this.pendingEvents.length >= ANALYTICS_CONFIG.BATCH_SIZE) {
      await this.flushEvents();
    }
  }

  async flushEvents() {
    if (this.pendingEvents.length === 0) return;

    try {
      await httpClient.post('/api/analytics/events', {
        events: this.pendingEvents
      });
      this.pendingEvents = [];
    } catch (error) {
      console.error('Error sending analytics:', error);
    }
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
      accountId,
      domain,
      action: 'start'
    });
  }

  async trackSessionEnd(accountId, domain) {
    await this.trackEvent({
      type: 'session',
      accountId,
      domain,
      action: 'end'
    });
  }
}

export const analyticsService = new AnalyticsService();