import { accountService } from './services/accountService.js';
import { sessionService } from './services/sessionService.js';
import { ui } from './utils/ui.js';

class AccountManager {
  constructor() {
    this.currentAccount = null;
    this.initializeEventListeners();
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
      await sessionService.updateSession(this.currentAccount.id, domain);
      sessionService.startInactivityTimer(domain, this.currentAccount.id);
    } catch (error) {
      console.error('Error handling tab activity:', error);
    }
  }

  async switchAccount(account) {
    try {
      // End current session if exists
      if (this.currentAccount) {
        await sessionService.endSession(this.currentAccount.id);
      }

      // Switch account
      const success = await accountService.switchAccount(account);
      if (!success) {
        throw new Error('Failed to switch account');
      }

      // Start new session
      const domain = this.getFirstDomain(account);
      if (domain) {
        await sessionService.startSession(account.id, domain);
        sessionService.startInactivityTimer(domain, account.id);
      }

      // Update state
      this.currentAccount = account;
      ui.showSuccess('Account switched successfully');

      // Refresh accounts list
      const accounts = await accountService.getAccounts();
      ui.updateAccountsList(accounts, account);

    } catch (error) {
      console.error('Error switching account:', error);
      ui.showError(error.message);
      throw error;
    }
  }

  getFirstDomain(account) {
    if (!account?.cookies?.length) return null;
    return account.cookies[0].domain.replace(/^\./, '');
  }
}

// Create and export a singleton instance
export const accountManager = new AccountManager();

// Make it available globally
window.accountManager = accountManager;