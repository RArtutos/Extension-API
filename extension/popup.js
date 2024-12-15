// Estado global
let currentAccount = null;
let proxyEnabled = false;

// Elementos DOM
const loginForm = document.getElementById('login-form');
const accountManager = document.getElementById('account-manager');
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const useProxyCheckbox = document.getElementById('use-proxy');
const accountsList = document.getElementById('accounts-list');

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
  chrome.storage.local.remove(['token', 'currentAccount'], function() {
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

async function switchAccount(account) {
  try {
    currentAccount = account;
    chrome.storage.local.set({ currentAccount: account });

    // Primero eliminar todas las cookies existentes de los dominios relevantes
    for (const cookie of account.cookies) {
      await chrome.cookies.remove({
        url: `https://${cookie.domain}`,
        name: cookie.name,
      });
    }

    // Luego establecer las nuevas cookies
    for (const cookie of account.cookies) {
      await chrome.cookies.set({
        url: `https://${cookie.domain}`,
        name: cookie.name,
        value: cookie.value,
        path: cookie.path,
        domain: cookie.domain,
        secure: true,
        sameSite: 'no_restriction'
      });
    }

    // Actualizar proxy si está habilitado
    if (proxyEnabled) {
      await updateProxy();
    }

    // Obtener el primer dominio para abrir
    if (account.cookies && account.cookies.length > 0) {
      const firstDomain = account.cookies[0].domain;
      // Abrir el dominio en una nueva pestaña
      chrome.tabs.create({ url: `https://${firstDomain}` });
    }

    // Actualizar UI
    updateAccountsListUI();

  } catch (error) {
    console.error('Error switching account:', error);
    alert('Error switching account. Check permissions and try again.');
  }
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
    updateAccountsListUI(accounts);

    // Cargar cuenta actual
    chrome.storage.local.get(['currentAccount'], result => {
      currentAccount = result.currentAccount;
      if (currentAccount) {
        updateAccountsListUI(accounts);
      }
    });
  } catch (error) {
    console.error('Failed to load accounts:', error);
  }
}

function updateAccountsListUI(accounts) {
  accountsList.innerHTML = accounts.map(account => {
    const isActive = currentAccount && currentAccount.name === account.name;
    return `
      <div class="account-item ${isActive ? 'active' : ''}">
        <span>${account.name}</span>
        <button class="switch-btn" data-account='${JSON.stringify(account)}'>Switch</button>
      </div>
    `;
  }).join('');

  // Agregar event listeners a los botones
  document.querySelectorAll('.switch-btn').forEach(button => {
    button.addEventListener('click', (e) => {
      const account = JSON.parse(e.target.dataset.account);
      switchAccount(account);
    });
  });
}

async function updateProxy() {
  // Implementar la lógica del proxy aquí si es necesario
  console.log('Updating proxy settings...');
}