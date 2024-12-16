import { api } from '../utils/api.js';
import { storage } from '../utils/storage.js';

class AnalyticsService {
    constructor() {
        this.activeTimers = new Map();
        this.INACTIVITY_TIMEOUT = 2 * 60 * 1000; // 2 minutes in milliseconds
    }

    async startSession(account) {
        try {
            await api.startSession(account.id);
            return true;
        } catch (error) {
            console.error('Error starting session:', error);
            return false;
        }
    }

    async endSession(account) {
        try {
            await api.endSession(account.id);
            return true;
        } catch (error) {
            console.error('Error ending session:', error);
            return false;
        }
    }

    startDomainTimer(domain, account) {
        if (this.activeTimers.has(domain)) {
            clearTimeout(this.activeTimers.get(domain));
        }

        const timer = setTimeout(async () => {
            await this.handleInactivity(domain, account);
        }, this.INACTIVITY_TIMEOUT);

        this.activeTimers.set(domain, timer);
    }

    async handleInactivity(domain, account) {
        console.log(`Domain ${domain} inactive for 2 minutes`);
        
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

        // End the session
        await this.endSession(account);
        
        this.activeTimers.delete(domain);
    }

    async updateActivity(domain, account) {
        try {
            await api.updateActivity(account.id, domain);
            this.startDomainTimer(domain, account);
        } catch (error) {
            console.error('Error updating activity:', error);
        }
    }

    async checkAccountStatus(account) {
        try {
            return await api.getAccountStatus(account.id);
        } catch (error) {
            console.error('Error checking account status:', error);
            return null;
        }
    }
}

export const analyticsService = new AnalyticsService();