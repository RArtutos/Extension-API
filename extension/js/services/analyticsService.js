import { api } from '../utils/api.js';
import { storage } from '../utils/storage.js';

class AnalyticsService {
    constructor() {
        this.activeTimers = new Map();
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
        }, 10 * 60 * 1000); // 10 minutes

        this.activeTimers.set(domain, timer);
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
    }

    resetTimer(domain) {
        this.startDomainTimer(domain);
    }
}

export const analyticsService = new AnalyticsService();