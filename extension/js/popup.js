import { accountService } from './services/accountService.js';
import { analyticsService } from './services/analyticsService.js';
import { ui } from './utils/ui.js';
import { storage } from './utils/storage.js';

// Initialize the app
document.addEventListener('DOMContentLoaded', async () => {
  const token = await storage.get('token');
  if (token) {
    ui.showAccountManager();
    await loadAccounts();
    await updateGlobalSessionInfo();
  } else {
    ui.showLoginForm();
  }
});

// Event Listeners
document.getElementById('login-btn').addEventListener('click', handleLogin);
document.getElementById('logout-btn').addEventListener('click', handleLogout);
document.getElementById('use-proxy').addEventListener('change', handleProxyToggle);
document.getElementById('view-stats').addEventListener('click', showStats);

async function handleLogin() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  try {
    await accountService.login(email, password);
    ui.showAccountManager();
    await loadAccounts();
  } catch (error) {
    ui.showError('Login failed: ' + error.message);
  }
}

async function handleLogout() {
  await accountService.logout();
  ui.showLoginForm();
}

async function loadAccounts() {
  try {
    const accounts = await accountService.getAccounts();
    const currentAccount = await accountService.getCurrentAccount();
    await ui.updateAccountsList(accounts, currentAccount);
  } catch (error) {
    ui.showError('Failed to load accounts: ' + error.message);
  }
}

async function updateGlobalSessionInfo() {
  const stats = await analyticsService.getGlobalStats();
  ui.updateGlobalSessionInfo(stats);
}

async function showStats() {
  const stats = await analyticsService.getDetailedStats();
  ui.showStatsModal(stats);
}

// Update session info periodically
setInterval(updateGlobalSessionInfo, 30000); // Every 30 seconds