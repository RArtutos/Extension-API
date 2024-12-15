import { REQUIRED_PERMISSIONS } from './config.js';
import { storage } from './storage.js';
import { api } from './api.js';
import { cookieManager } from './cookies.js';
import { ui } from './ui.js';

let currentAccount = null;
let proxyEnabled = false;

// Inicialización
async function init() {
  const token = await storage.get('token');
  if (token) {
    ui.showAccountManager();
    loadAccounts();
  } else {
    ui.showLoginForm();
  }
}

// Event Listeners
document.getElementById('login-btn').addEventListener('click', async () => {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  try {
    const data = await api.login(email, password);
    if (data.access_token) {
      await storage.set('token', data.access_token);
      ui.showAccountManager();
      loadAccounts();
    }
  } catch (error) {
    console.error('Login failed:', error);
    ui.showError('Login failed. Please try again.');
  }
});

document.getElementById('logout-btn').addEventListener('click', async () => {
  await storage.remove(['token', 'currentAccount']);
  ui.showLoginForm();
});

document.getElementById('use-proxy').addEventListener('change', (e) => {
  proxyEnabled = e.target.checked;
  if (currentAccount) {
    updateProxy();
  }
});

// Funciones principales
async function loadAccounts() {
  try {
    const token = await storage.get('token');
    const accounts = await api.getAccounts(token);
    currentAccount = await storage.get('currentAccount');
    ui.updateAccountsList(accounts, currentAccount);
    
    // Agregar event listeners a los botones
    document.querySelectorAll('.switch-btn').forEach(button => {
      button.addEventListener('click', (e) => {
        const account = JSON.parse(e.target.dataset.account);
        switchAccount(account);
      });
    });
  } catch (error) {
    console.error('Failed to load accounts:', error);
    ui.showError('Failed to load accounts. Please try again.');
  }
}

async function switchAccount(account) {
  try {
    // Solicitar permisos primero
    const granted = await cookieManager.requestPermissions();
    if (!granted) {
      throw new Error('Required permissions were not granted');
    }

    currentAccount = account;
    await storage.set('currentAccount', account);

    // Manejar cookies
    const errors = [];
    for (const cookie of account.cookies) {
      try {
        const url = `https://${cookie.domain}`;
        await cookieManager.removeCookie(url, cookie.name);
        await cookieManager.setCookie(cookie);
      } catch (error) {
        errors.push(`Cookie ${cookie.name}: ${error.message}`);
      }
    }

    // Si hay errores pero no son críticos, continuamos
    if (errors.length > 0) {
      console.warn('Some cookies could not be set:', errors);
    }

    // Actualizar proxy si está habilitado
    if (proxyEnabled) {
      await updateProxy();
    }

    // Abrir primera página
    if (account.cookies && account.cookies.length > 0) {
      const firstDomain = account.cookies[0].domain;
      chrome.tabs.create({ url: `https://${firstDomain}` });
    }

    // Actualizar UI
    ui.updateAccountsList(await api.getAccounts(await storage.get('token')), currentAccount);

    // Mostrar mensaje de éxito
    ui.showError('Account switched successfully' + (errors.length > 0 ? ' (some cookies were skipped)' : ''));

  } catch (error) {
    console.error('Error switching account:', error);
    ui.showError('Error switching account: ' + error.message);
  }
}

async function updateProxy() {
  // Implementar la lógica del proxy aquí si es necesario
  console.log('Updating proxy settings...');
}

// Iniciar la aplicación
init();