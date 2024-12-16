class UI {
  showLoginForm() {
    this._showElement('login-form');
    this._hideElement('account-manager');
  }

  showAccountManager() {
    this._hideElement('login-form');
    this._showElement('account-manager');
  }

  updateAccountsList(accounts, currentAccount) {
    const accountsList = document.getElementById('accounts-list');
    if (!accountsList) return;

    accountsList.innerHTML = accounts.map(account => {
      const isActive = currentAccount && currentAccount.id === account.id;
      const sessionInfo = `${account.active_sessions}/${account.max_concurrent_users} users`;
      const isDisabled = account.active_sessions >= account.max_concurrent_users && !isActive;
      
      return `
        <div class="account-item ${isActive ? 'active' : ''} ${isDisabled ? 'disabled' : ''}">
          <div class="account-info">
            <span class="account-name">${account.name}</span>
            <span class="account-group">${account.group || ''}</span>
            <span class="session-info">${sessionInfo}</span>
          </div>
          <button class="switch-btn" 
                  data-account='${JSON.stringify(account)}'
                  ${isDisabled ? 'disabled' : ''}>
            ${isActive ? 'Current' : 'Switch'}
          </button>
        </div>
      `;
    }).join('');

    this.attachSwitchButtonListeners();
  }

  attachSwitchButtonListeners() {
    document.querySelectorAll('.switch-btn').forEach(button => {
      button.addEventListener('click', async (e) => {
        const account = JSON.parse(e.target.dataset.account);
        const { accountManager } = await import('../accountManager.js');
        accountManager.switchAccount(account);
      });
    });
  }

  showError(message) {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
      errorDiv.textContent = message;
      errorDiv.classList.remove('hidden');
      setTimeout(() => errorDiv.classList.add('hidden'), 5000);
    } else {
      console.error(message);
    }
  }

  showSuccess(message) {
    const successDiv = document.getElementById('success-message');
    if (successDiv) {
      successDiv.textContent = message;
      successDiv.classList.remove('hidden');
      setTimeout(() => successDiv.classList.add('hidden'), 3000);
    } else {
      console.log(message);
    }
  }

  _showElement(id) {
    const element = document.getElementById(id);
    if (element) element.classList.remove('hidden');
  }

  _hideElement(id) {
    const element = document.getElementById(id);
    if (element) element.classList.add('hidden');
  }
}

export const ui = new UI();