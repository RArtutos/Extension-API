import { storage } from './utils/storage.js';
import { accountService } from './services/accountService.js';
import { sessionService } from './services/sessionService.js';
import { ui } from './utils/ui.js';

class AccountManager {
    constructor() {
        this.proxyEnabled = false;
        this.initializeEventListeners();
    }

    async init() {
        const token = await storage.get('token');
        if (token) {
            ui.showAccountManager();
            this.loadAccounts();
        } else {
            ui.showLoginForm();
        }
    }

    initializeEventListeners() {
        // Listen for tab updates to track activity
        chrome.tabs.onActivated.addListener(async (activeInfo) => {
            const tab = await chrome.tabs.get(activeInfo.tabId);
            if (tab.url) {
                const domain = new URL(tab.url).hostname;
                const currentAccount = await storage.get('currentAccount');
                if (currentAccount) {
                    await sessionService.resetTimer(domain, currentAccount.id);
                }
            }
        });

        chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
            if (changeInfo.url) {
                const domain = new URL(changeInfo.url).hostname;
                const currentAccount = await storage.get('currentAccount');
                if (currentAccount) {
                    await sessionService.resetTimer(domain, currentAccount.id);
                }
            }
        });
    }

    async loadAccounts() {
        try {
            const accounts = await accountService.loadAccounts();
            const currentAccount = await accountService.getCurrentAccount();
            ui.updateAccountsList(accounts, currentAccount);
        } catch (error) {
            console.error('Failed to load accounts:', error);
            ui.showError('Error loading accounts. Please try again.');
        }
    }

    async switchAccount(account) {
        try {
            console.log('Switching to account:', account);

            // Check session limits
            const sessionInfo = await accountService.getSessionInfo(account.id);
            if (sessionInfo.active_sessions >= sessionInfo.max_concurrent_users) {
                throw new Error(`This account has reached its maximum number of concurrent users (${sessionInfo.max_concurrent_users}). Please try another account.`);
            }

            // Remove current account cookies and session
            const currentAccount = await accountService.getCurrentAccount();
            if (currentAccount) {
                for (const cookie of currentAccount.cookies) {
                    await accountService.removeAllCookies(cookie.domain);
                }
                await sessionService.removeSession(currentAccount.id);
            }

            // Set new account cookies and create session
            const firstDomain = accountService.getFirstDomain(account);
            if (firstDomain) {
                const sessionCreated = await sessionService.createSession(account.id, firstDomain);
                if (!sessionCreated) {
                    throw new Error('Failed to create session. Please try again.');
                }

                for (const cookie of account.cookies) {
                    await accountService.setCookies(cookie);
                }
                await sessionService.startInactivityTimer(firstDomain, account.id);
            }

            // Update storage and UI
            await storage.set('currentAccount', account);
            const accounts = await accountService.loadAccounts();
            ui.updateAccountsList(accounts, account);

            // Open first page if available
            if (firstDomain) {
                chrome.tabs.create({ url: `https://${firstDomain}` });
            }

            ui.showSuccess('Account switched successfully');
        } catch (error) {
            console.error('Error switching account:', error);
            ui.showError(error.message);
        }
    }
}

export const accountManager = new AccountManager();