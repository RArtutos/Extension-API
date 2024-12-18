import { isTabForAccount } from './domain-utils.js';

export class TabMonitor {
  constructor(onAllTabsClosed) {
    this.onAllTabsClosed = onAllTabsClosed;
    this.initialize();
  }

  initialize() {
    chrome.tabs.onRemoved.addListener(() => this.checkTabs());
  }

  async checkTabs() {
    try {
      const tabs = await chrome.tabs.query({});
      const hasOpenTabs = tabs.some(tab => isTabForAccount(tab, this.currentAccount));
      
      if (!hasOpenTabs) {
        await this.onAllTabsClosed();
      }
    } catch (error) {
      console.error('Error checking tabs:', error);
    }
  }
}