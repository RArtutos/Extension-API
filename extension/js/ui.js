export const ui = {
  showLoginForm() {
    document.getElementById('login-form').classList.remove('hidden');
    document.getElementById('account-manager').classList.add('hidden');
  },

  showAccountManager() {
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('account-manager').classList.remove('hidden');
  },

  updateAccountsList(accounts, currentAccount) {
    const accountsList = document.getElementById('accounts-list');
    accountsList.innerHTML = accounts.map(account => {
      const isActive = currentAccount && currentAccount.name === account.name;
      return `
        <div class="account-item ${isActive ? 'active' : ''}">
          <span>${account.name}</span>
          <button class="switch-btn" data-account='${JSON.stringify(account)}'>Switch</button>
        </div>
      `;
    }).join('');
  },

  showError(message) {
    alert(message);
  }
};