import { api } from '../utils/api.js';
import { storage } from '../utils/storage.js';
import { STORAGE_KEYS } from '../config.js';

class SessionService {
    constructor() {
        this.activeTimers = new Map();
    }

    async createSession(accountId, domain) {
        const token = await storage.get(STORAGE_KEYS.TOKEN);
        if (!token) return false;

        try {
            const response = await api.createSession(accountId, domain);
            return response.success;
        } catch (error) {
            console.error('Error creating session:', error);
            return false;
        }
    }

    async updateSession(accountId, domain) {
        const token = await storage.get(STORAGE_KEYS.TOKEN);
        if (!token) return false;

        try {
            const response = await api.updateSession(accountId, domain);
            return response.success;
        } catch (error) {
            console.error('Error updating session:', error);
            return false;
        }
    }

    startInactivityTimer(domain, accountId) {
        if (this.activeTimers.has(domain)) {
            clearTimeout(this.activeTimers.get(domain));
        }

        const timer = setTimeout(async () => {
            await this.handleInactivity(domain, accountId);
        }, 60000); // 1 minute

        this.activeTimers.set(domain, timer);
    }

    async handleInactivity(domain, accountId) {
        const currentAccount = await storage.get(STORAGE_KEYS.CURRENT_ACCOUNT);
        if (!currentAccount || currentAccount.id !== accountId) return;

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
        await api.removeSession(accountId, domain);
    }

    resetTimer(domain, accountId) {
        this.startInactivityTimer(domain, accountId);
        this.updateSession(accountId, domain);
    }
}

export const sessionService = new SessionService();