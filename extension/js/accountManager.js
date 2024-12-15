```javascript
import { cookieManager } from './cookies.js';
import { storage } from './storage.js';
import { api } from './api.js';
import { ui } from './ui.js';

class AccountManager {
  constructor() {
    this.currentAccount = null;
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
      const token = await storage.get('token');
      const accounts = await api.getAccounts(token);
      this.currentAccount = await storage.get('currentAccount');
      ui.updateAccountsList(accounts, this.currentAccount);
    } catch (error) {
      console.error('Failed to load accounts:', error);
      ui.showError('Error al cargar las cuentas. Por favor, intenta de nuevo.');
    }
  }

  async switchAccount(account) {
    try {
      console.log('Switching to account:', account); // Debug

      const granted = await cookieManager.requestPermissions();
      if (!granted) {
        throw new Error('No se otorgaron los permisos necesarios');
      }

      this.currentAccount = account;
      await storage.set('currentAccount', account);

      // Procesar cookies
      for (const cookie of account.cookies) {
        console.log('Processing cookie:', cookie); // Debug
        
        const domain = cookie.domain;
        
        // Primero eliminamos las cookies existentes
        const existingCookies = await chrome.cookies.getAll({ domain });
        console.log('Existing cookies:', existingCookies); // Debug
        
        for (const existing of existingCookies) {
          await chrome.cookies.remove({
            url: `https://${domain}`,
            name: existing.name
          });
        }

        // Procesar el header string de cookies
        if (cookie.name === 'header_cookies') {
          const cookieString = cookie.value;
          console.log('Cookie string to process:', cookieString); // Debug
          
          const cookiePairs = cookieString.split(';');
          for (const pair of cookiePairs) {
            const trimmedPair = pair.trim();
            if (!trimmedPair) continue;

            const firstEquals = trimmedPair.indexOf('=');
            if (firstEquals === -1) continue;

            const name = trimmedPair.substring(0, firstEquals).trim();
            const value = trimmedPair.substring(firstEquals + 1).trim();

            if (!name || !value) continue;

            console.log('Setting cookie:', { name, value, domain }); // Debug

            try {
              await chrome.cookies.set({
                url: `https://${domain}`,
                domain: domain,
                name: name,
                value: value,
                path: '/',
                secure: true,
                sameSite: 'no_restriction'
              });
            } catch (error) {
              console.error(`Error setting cookie ${name}:`, error);
            }
          }
        }
      }

      // Abrir primera página
      if (account.cookies && account.cookies.length > 0) {
        const firstDomain = account.cookies[0].domain;
        const url = `https://${firstDomain.replace(/^\./, '')}`;
        console.log('Opening URL:', url); // Debug
        chrome.tabs.create({ url });
      }

      // Actualizar UI
      const accounts = await api.getAccounts(await storage.get('token'));
      ui.updateAccountsList(accounts, this.currentAccount);

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
    if (this.currentAccount) {
      this.updateProxy();
    }
  }
}

export const accountManager = new AccountManager();
```