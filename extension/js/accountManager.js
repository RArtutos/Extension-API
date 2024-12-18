import { accountService } from './services/accountService.js';
import { sessionService } from './services/sessionService.js';
import { cookieManager } from './utils/cookieManager.js';
import { analyticsService } from './services/analyticsService.js';
import { ui } from './utils/ui.js';

class AccountManager {
  constructor() {
    this.currentAccount = null;
    this.initializeEventListeners();
  }

  initializeEventListeners() {
    // Monitor tab activity
    chrome.tabs.onActivated.addListener(async (activeInfo) => {
      const tab = await chrome.tabs.get(activeInfo.tabId);
      if (tab.url) {
        const domain = new URL(tab.url).hostname;
        await this.handleTabActivity(domain);
      }
    });

    // Monitor URL changes
    chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
      if (changeInfo.url) {
        const oldDomain = this.currentAccount?.cookies[0]?.domain;
        const newDomain = new URL(changeInfo.url).hostname;
        
        // If user navigates away from the account domain
        if (oldDomain && !newDomain.includes(oldDomain.replace(/^\./, ''))) {
          await this.handleDomainExit(oldDomain);
        }
        
        await this.handleTabActivity(newDomain);
      }
    });
  }

  async handleTabActivity(domain) {
    if (!this.currentAccount) return;

    try {
      await sessionService.updateSession(this.currentAccount.id, domain);
      await analyticsService.trackPageView(domain);
    } catch (error) {
      console.error('Error handling tab activity:', error);
      ui.showError('Error updating session activity');
    }
  }

  async handleDomainExit(domain) {
    if (!this.currentAccount) return;

    try {
      await cookieManager.removeAccountCookies(this.currentAccount);
      await sessionService.endSession(this.currentAccount.id, domain);
      this.currentAccount = null;
      await storage.remove('currentAccount');
    } catch (error) {
      console.error('Error handling domain exit:', error);
    }
  }

  async switchAccount(account) {
    try {
      // Check session limits
      const sessionInfo = await sessionService.getSessionInfo(account.id);
      if (sessionInfo.active_sessions >= sessionInfo.max_concurrent_users) {
        throw new Error(`Maximum concurrent users (${sessionInfo.max_concurrent_users}) reached for this account`);
      }

      // End current session if exists
      if (this.currentAccount) {
        const currentDomain = this.currentAccount.cookies[0]?.domain;
        await sessionService.endSession(this.currentAccount.id, currentDomain);
        await cookieManager.removeAccountCookies(this.currentAccount);
      }

      // Set new cookies
      await cookieManager.setAccountCookies(account);

      // Start new session
      const domain = this.getFirstDomain(account);
      if (domain) {
        await sessionService.startSession(account.id, domain);
        
        // Track account switch
        await analyticsService.trackAccountSwitch(this.currentAccount, account);
        
        // Open the domain in a new tab
        chrome.tabs.create({ url: `https://${domain}` });
      }

      // Update state
      this.currentAccount = account;
      await storage.set('currentAccount', account);
      
      ui.showSuccess('Account switched successfully');

      // Refresh accounts list
      const accounts = await accountService.getAccounts();
      ui.updateAccountsList(accounts, account);

    } catch (error) {
      console.error('Error switching account:', error);
      ui.showError(error.message || 'Error switching account');
      throw error;
    }
  }

  getFirstDomain(account) {
    if (!account?.cookies?.length) return null;
    const domain = account.cookies[0].domain;
    return domain.startsWith('.') ? domain.substring(1) : domain;
  }
}

export const accountManager = new AccountManager();