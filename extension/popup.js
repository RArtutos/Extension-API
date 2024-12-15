// Estado global
let currentAccount = null;
let proxyEnabled = false;

// Elementos DOM
const loginForm = document.getElementById('login-form');
const accountManager = document.getElementById('account-manager');
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const useProxyCheckbox = document.getElementById('use-proxy');

// Verificar estado de autenticación al cargar
chrome.storage.local.get(['token'], function(result) {
  if (result.token) {
    showAccountManager();
    loadAccounts();
  } else {
    showLoginForm();
  }
});

// Event Listeners
loginBtn.addEventListener('click', async () => {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  try {
    const response = await fetch('http://84.46.249.121:8000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
    });

    const data = await response.json();
    if (data.access_token) {
      chrome.storage.local.set({ token: data.access_token }, function() {
        showAccountManager();
        loadAccounts();
      });
    }
  } catch (error) {
    console.error('Login failed:', error);
  }
});

logoutBtn.addEventListener('click', () => {
  chrome.storage.local.remove(['token'], function() {
    showLoginForm();
  });
});

useProxyCheckbox.addEventListener('change', (e) => {
  proxyEnabled = e.target.checked;
  if (currentAccount) {
    updateProxy();
  }
});

// Funciones auxiliares
function showLoginForm() {
  loginForm.classList.remove('hidden');
  accountManager.classList.add('hidden');
}

function showAccountManager() {
  loginForm.classList.add('hidden');
  accountManager.classList.remove('hidden');
}

async function loadAccounts() {
  try {
    const token = await new Promise(resolve => {
      chrome.storage.local.get(['token'], result => resolve(result.token));
    });

    const response = await fetch('http://84.46.249.121:8000/api/accounts', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    const accounts = await response.json();
    const accountsList = document.getElementById('accounts-list');
    accountsList.innerHTML = accounts.map(account => `
      <div class="account-item">
        <span>${account.name}</span>
        <button onclick="switchAccount(${account.id})">Switch</button>
      </div>
    `).join('');
  } catch (error) {
    console.error('Failed to load accounts:', error);
  }
}

async function switchAccount(accountId) {
  try {
    const token = await new Promise(resolve => {
      chrome.storage.local.get(['token'], result => resolve(result.token));
    });

    const response = await fetch(`http://84.46.249.121:8000/api/accounts/${accountId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    const account = await response.json();
    currentAccount = account;

    // Aplicar cookies
    for (const cookie of account.cookies) {
      await chrome.cookies.set({
        url: `https://${cookie.domain}`,
        name: cookie.name,
        value: cookie.value,
        path: cookie.path,
        domain: cookie.domain,
      });
    }

    // Actualizar proxy si está habilitado
    if (proxyEnabled) {
      updateProxy();
    }
  } catch (error) {
    console.error('Failed to switch account:', error);
  }
}

async function updateProxy() {
  if (!currentAccount || !proxyEnabled) {
    // Deshabilitar proxy
    await chrome.proxy.settings.clear({
      scope: 'regular',
    });
    return;
  }

  try {
    const token = await new Promise(resolve => {
      chrome.storage.local.get(['token'], result => resolve(result.token));
    });

    const response = await fetch('http://84.46.249.121:8000/api/proxies', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    const proxies = await response.json();
    if (proxies.length > 0) {
      const proxy = proxies[0]; // Usar el primer proxy disponible
      
      const config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: proxy.type,
            host: proxy.host,
            port: proxy.port,
          },
        },
      };

      if (proxy.username && proxy.password) {
        config.rules.singleProxy.username = proxy.username;
        config.rules.singleProxy.password = proxy.password;
      }

      await chrome.proxy.settings.set({
        value: config,
        scope: 'regular',
      });
    }
  } catch (error) {
    console.error('Failed to update proxy:', error);
  }
}