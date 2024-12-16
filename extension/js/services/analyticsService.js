import { api } from '../utils/api.js';
import { storage } from '../utils/storage.js';

class AnalyticsService {
    constructor() {
        this.activeTimers = new Map();
        this.INACTIVITY_TIMEOUT = 5 * 60 * 1000; // 5 minutos
    }

    async logAccess(domain, action) {
        const token = await storage.get('token');
        const currentAccount = await storage.get('currentAccount');

        if (!token || !currentAccount) return;

        try {
            await api.logAccess({
                domain,
                action,
                accountId: currentAccount.id
            });
        } catch (error) {
            console.error('Error logging access:', error);
        }
    }

    startDomainTimer(domain) {
        if (this.activeTimers.has(domain)) {
            clearTimeout(this.activeTimers.get(domain));
        }

        const timer = setTimeout(async () => {
            await this.handleInactivity(domain);
        }, this.INACTIVITY_TIMEOUT);

        this.activeTimers.set(domain, timer);
        this.updateLastActivity(domain);
    }

    async updateLastActivity(domain) {
        const currentAccount = await storage.get('currentAccount');
        if (!currentAccount) return;

        try {
            await api.updateActivity({
                accountId: currentAccount.id,
                domain: domain,
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            console.error('Error updating activity:', error);
        }
    }

    async handleInactivity(domain) {
        const currentAccount = await storage.get('currentAccount');
        if (!currentAccount) return;

        // Remove cookies for the inactive domain
        const cookies = await chrome.cookies.getAll({ domain });
        for (const cookie of cookies) {
            try {
                await chrome.cookies.remove({
                    url: `https://${domain}`,
                    name: cookie.name
                });
            } catch (error) {
                console.error(`Error removing cookie ${cookie.name}:`, error);
            }
        }

        this.activeTimers.delete(domain);
        await this.logAccess(domain, 'timeout');
        
        // Notify the backend about session end
        try {
            await api.endSession({
                accountId: currentAccount.id,
                domain: domain
            });
        } catch (error) {
            console.error('Error ending session:', error);
        }
    }

    resetTimer(domain) {
        this.startDomainTimer(domain);
    }
}

export const analyticsService = new AnalyticsService();