import { storage } from './utils/storage.js';
import { accountService } from './services/accountService.js';
import { analyticsService } from './services/analyticsService.js';
import { ui } from './utils/ui.js';

class AccountManager {
    constructor() {
        this.proxyEnabled = false;
        this.currentAccount = null;
        this.updateInterval = null;
    }

    async init() {
        const token = await storage.get('token');
        if (token) {
            ui.showAccountManager();
            await this.loadAccounts();
            this.startStatusUpdates();
        } else {
            ui.showLoginForm();
        }
    }

    async loadAccounts() {
        try {
            const accounts = await accountService.loadAccounts();
            this.currentAccount = await accountService.getCurrentAccount();
            
            // Get real-time status for each account
            for (const account of accounts) {
                const status = await analyticsService.checkAccountStatus(account);
                if (status) {
                    account.active_sessions = status.active_sessions;
                    account.max_concurrent_users = status.max_concurrent_users;
                    account.active_users = status.active_users;
                }
            }
            
            ui.updateAccountsList(accounts, this.currentAccount);
        } catch (error) {
            console.error('Failed to load accounts:', error);
            ui.showError('Error loading accounts. Please try again.');
        }
    }

    startStatusUpdates() {
        // Update account status every minute
        this.updateInterval = setInterval(() => {
            if (this.currentAccount) {
                this.updateAccountStatus();
            }
        }, 60000); // 1 minute
    }

    async updateAccountStatus() {
        try {
            const status = await analyticsService.checkAccountStatus(this.currentAccount);
            if (status) {
                ui.updateAccountStatus(status);
            }
        } catch (error) {
            console.error('Error updating account status:', error);
        }
    }

    async switchAccount(account) {
        try {
            // Check if account has reached maximum users
            const status = await analyticsService.checkAccountStatus(account);
            if (status && status.active_sessions >= status.max_concurrent_users) {
                ui.showError(`Cannot switch to account: Maximum users (${status.max_concurrent_users}) reached`);
                return;
            }

            console.log('Switching to account:', account);

            // End current session if exists
            if (this.currentAccount) {
                await analyticsService.endSession(this.currentAccount);
            }

            // Start new session
            const sessionStarted = await analyticsService.startSession(account);
            if (!sessionStarted) {
                throw new Error('Failed to start session');
            }

            await accountService.switchAccount(account);
            this.currentAccount = account;

            // Open first page if available
            const firstDomain = accountService.getFirstDomain(account);
            if (firstDomain) {
                chrome.tabs.create({ url: `https://${firstDomain}` });
            }

            // Update UI
            const accounts = await accountService.loadAccounts();
            ui.updateAccountsList(accounts, account);

            ui.showSuccess('Account switched successfully');
        } catch (error) {
            console.error('Error switching account:', error);
            ui.showError('Error switching account: ' + error.message);
        }
    }

    cleanup() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    }
}

export const accountManager = new AccountManager();