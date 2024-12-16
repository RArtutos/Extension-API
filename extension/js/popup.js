import { accountManager } from './accountManager.js';
import { storage } from './utils/storage.js';
import { api } from './utils/api.js';
import { ui } from './utils/ui.js';

// Event Listeners
document.getElementById('login-btn').addEventListener('click', async () => {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  try {
    const data = await api.login(email, password);
    if (data.access_token) {
      await storage.set('token', data.access_token);
      accountManager.init();
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
  accountManager.setProxyEnabled(e.target.checked);
});

// Initialize the application
accountManager.init();