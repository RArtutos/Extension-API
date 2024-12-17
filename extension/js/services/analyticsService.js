import { api } from '../utils/api.js';
import { storage } from '../utils/storage.js';
import { ANALYTICS_CONFIG } from '../config.js';

class AnalyticsService {
    constructor() {
        this.pendingEvents = [];
        this.initializeTracking();
    }

    async initializeTracking() {
        // Start periodic tracking
        setInterval(() => this.flushEvents(), ANALYTICS_CONFIG.TRACKING_INTERVAL);
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

        const events = [...this.pendingEvents];
        this.pendingEvents = [];

        try {
            const token = await storage.get('token');
            if (!token) return;

            await api.post('/analytics/events', { events }, token);
        } catch (error) {
            console.error('Error sending analytics:', error);
            // Requeue failed events
            this.pendingEvents = [...events, ...this.pendingEvents];
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