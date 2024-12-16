import { storage } from './utils/storage.js';
import { accountService } from './services/accountService.js';
import { ui } from './utils/ui.js';

class AccountManager {
  constructor() {
    this.proxyEnabled = false;
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

  async loadAccounts() {
    try {
      const accounts = await accountService.loadAccounts();
      const currentAccount = await accountService.getCurrentAccount();
      ui.updateAccountsList(accounts, currentAccount);
    } catch (error) {
      console.error('Failed to load accounts:', error);
      ui.showError('Error al cargar las cuentas. Por favor, intenta de nuevo.');
    }
  }

  async switchAccount(account) {
    try {
      console.log('Switching to account:', account);

      await accountService.switchAccount(account);

      // Open first page if available
      const firstDomain = accountService.getFirstDomain(account);
      if (firstDomain) {
        chrome.tabs.create({ url: `https://${firstDomain}` });
      }

      // Update UI
      const accounts = await accountService.loadAccounts();
      ui.updateAccountsList(accounts, account);

      ui.showSuccess('Cuenta cambiada exitosamente');
    } catch (error) {
      console.error('Error switching account:', error);
      ui.showError('Error al cambiar de cuenta: ' + error.message);
    }
  }

  async updateProxy() {
    console.log('Actualizando configuración del proxy...');
  }

  setProxyEnabled(enabled) {
    this.proxyEnabled = enabled;
    if (accountService.getCurrentAccount()) {
      this.updateProxy();
    }
  }
}

export const accountManager = new AccountManager();