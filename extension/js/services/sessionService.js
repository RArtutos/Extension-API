import { api } from '../utils/api.js';
import { storage } from '../utils/storage.js';
import { cookieService } from './cookieService.js';

class SessionService {
    constructor() {
        this.activeTimers = new Map();
    }

    async createSession(accountId, domain) {
        try {
            const response = await api.createSession(accountId, domain);
            return response.success;
        } catch (error) {
            console.error('Error creating session:', error);
            return false;
        }
    }

    async updateSession(accountId, domain) {
        try {
            const response = await api.updateSession(accountId, domain);
            return response.success;
        } catch (error) {
            console.error('Error updating session:', error);
            return false;
        }
    }

    async removeSession(accountId) {
        try {
            const response = await api.removeSession(accountId);
            return response.success;
        } catch (error) {
            console.error('Error removing session:', error);
            return false;
        }
    }

    startInactivityTimer(domain, accountId) {
        if (this.activeTimers.has(domain)) {
            clearTimeout(this.activeTimers.get(domain));
        }

        const timer = setTimeout(async () => {
            await this.handleInactivity(domain, accountId);
        }, 60000); // 1 minute inactivity timeout

        this.activeTimers.set(domain, timer);
    }

    async handleInactivity(domain, accountId) {
        const currentAccount = await storage.get('currentAccount');
        if (!currentAccount || currentAccount.id !== accountId) return;

        console.log(`Handling inactivity for domain: ${domain}`);

        // Remove cookies only for the inactive domain
        await cookieService.removeAllCookies(domain);
        
        this.activeTimers.delete(domain);
        await this.updateSession(accountId, domain);
    }

    async resetTimer(domain, accountId) {
        this.startInactivityTimer(domain, accountId);
        await this.updateSession(accountId, domain);
    }
}

export const sessionService = new SessionService();