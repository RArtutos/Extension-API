import { accountManager } from './accountManager.js';
import { ui } from './utils/ui.js';

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  accountManager.init();
  attachEventListeners();
});

function attachEventListeners() {
  // Login form
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      await accountManager.login(email, password);
    });
  }

  // Logout button
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => accountManager.logout());
  }

  // Proxy toggle
  const proxyToggle = document.getElementById('use-proxy');
  if (proxyToggle) {
    proxyToggle.addEventListener('change', (e) => {
      accountManager.setProxyEnabled(e.target.checked);
    });
  }

  // Stats button
  const statsBtn = document.getElementById('view-stats');
  if (statsBtn) {
    statsBtn.addEventListener('click', () => accountManager.showStats());
  }
}