import { storage } from './utils/storage.js';
import { api } from './utils/api.js';
import { ui } from './utils/ui.js';
import { analyticsService } from './services/analyticsService.js';
import { SESSION_CONFIG } from './config.js';

class AccountManager {
    constructor() {
        this.currentAccount = null;
        this.activeTimers = new Map();
        this.initializeEventListeners();
    }

    async init() {
        try {
            const token = await storage.get('token');
            if (!token) {
                ui.showLoginForm();
                return;
            }

            ui.showAccountManager();
            await this.loadAccounts();
            await this.restoreSession();
        } catch (error) {
            console.error('Initialization error:', error);
            ui.showError('Failed to initialize. Please try again.');
        }
    }

    async restoreSession() {
        const currentAccount = await storage.get('currentAccount');
        if (currentAccount) {
            await this.switchAccount(currentAccount, true);
        }
    }

    initializeEventListeners() {
        chrome.tabs.onActivated.addListener(async (activeInfo) => {
            const tab = await chrome.tabs.get(activeInfo.tabId);
            if (tab.url) {
                const domain = new URL(tab.url).hostname;
                await this.handleTabActivity(domain);
            }
        });

        chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
            if (changeInfo.url) {
                const domain = new URL(changeInfo.url).hostname;
                await this.handleTabActivity(domain);
            }
        });
    }

    async handleTabActivity(domain) {
        if (!this.currentAccount) return;

        try {
            await analyticsService.trackPageView(domain);
            await this.resetSessionTimer(domain);
        } catch (error) {
            console.error('Error handling tab activity:', error);
        }
    }

    async loadAccounts() {
        try {
            const accounts = await api.getAccounts();
            const currentAccount = await storage.get('currentAccount');
            ui.updateAccountsList(accounts, currentAccount);
            return accounts;
        } catch (error) {
            console.error('Error loading accounts:', error);
            ui.showError('Failed to load accounts');
            return [];
        }
    }

    async switchAccount(account, isRestore = false) {
        try {
            // Verify session limits
            const sessionInfo = await api.getSessionInfo(account.id);
            if (!isRestore && sessionInfo.active_sessions >= sessionInfo.max_concurrent_users) {
                throw new Error(`Maximum concurrent users (${sessionInfo.max_concurrent_users}) reached`);
            }

            // End current session if exists
            if (this.currentAccount) {
                await this.endCurrentSession();
            }

            // Start new session
            const success = await this.startNewSession(account);
            if (!success) {
                throw new Error('Failed to start new session');
            }

            // Track account switch
            await analyticsService.trackAccountSwitch(this.currentAccount, account);

            // Update state
            this.currentAccount = account;
            await storage.set('currentAccount', account);
            
            // Refresh UI
            const accounts = await this.loadAccounts();
            ui.updateAccountsList(accounts, account);

            if (!isRestore) {
                ui.showSuccess('Account switched successfully');
            }
        } catch (error) {
            console.error('Error switching account:', error);
            ui.showError(error.message);
            throw error;
        }
    }

    async startNewSession(account) {
        try {
            const domain = this.getFirstDomain(account);
            if (!domain) return false;

            await analyticsService.trackSessionStart(account.id, domain);
            await this.resetSessionTimer(domain);

            return true;
        } catch (error) {
            console.error('Error starting session:', error);
            return false;
        }
    }

    async endCurrentSession() {
        if (!this.currentAccount) return;

        try {
            const domain = this.getFirstDomain(this.currentAccount);
            if (domain) {
                await analyticsService.trackSessionEnd(this.currentAccount.id, domain);
            }

            // Clear timers
            this.activeTimers.forEach(timer => clearTimeout(timer));
            this.activeTimers.clear();

        } catch (error) {
            console.error('Error ending session:', error);
        }
    }

    async resetSessionTimer(domain) {
        if (!this.currentAccount) return;

        // Clear existing timer
        if (this.activeTimers.has(domain)) {
            clearTimeout(this.activeTimers.get(domain));
        }

        // Set new timer
        const timer = setTimeout(
            () => this.handleSessionTimeout(domain),
            SESSION_CONFIG.INACTIVITY_TIMEOUT
        );

        this.activeTimers.set(domain, timer);

        // Update session activity
        try {
            await api.updateSession(this.currentAccount.id, domain);
        } catch (error) {
            console.error('Error updating session:', error);
        }
    }

    async handleSessionTimeout(domain) {
        if (!this.currentAccount) return;

        try {
            await analyticsService.trackSessionEnd(this.currentAccount.id, domain);
            this.activeTimers.delete(domain);
            
            // Check if this was the last active domain
            if (this.activeTimers.size === 0) {
                await this.endCurrentSession();
                await storage.remove('currentAccount');
                this.currentAccount = null;
                ui.showSessionExpired();
            }
        } catch (error) {
            console.error('Error handling session timeout:', error);
        }
    }

    getFirstDomain(account) {
        if (!account?.cookies?.length) return null;
        return account.cookies[0].domain.replace(/^\./, '');
    }
}

export const accountManager = new AccountManager();