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
            const isActive = currentAccount && currentAccount.id === account.id;
            const isDisabled = account.active_sessions >= account.max_concurrent_users && !isActive;
            
            return `
                <div class="account-item ${isActive ? 'active' : ''} ${isDisabled ? 'disabled' : ''}">
                    <div class="account-info">
                        <div class="account-name">${account.name}</div>
                        ${account.group ? `<div class="account-group">${account.group}</div>` : ''}
                        <div class="session-info">
                            <span class="badge bg-${account.active_sessions >= account.max_concurrent_users ? 'danger' : 'success'}">
                                ${account.active_sessions}/${account.max_concurrent_users} users
                            </span>
                        </div>
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
    },

    attachSwitchButtonListeners() {
        document.querySelectorAll('.switch-btn').forEach(button => {
            button.addEventListener('click', async (e) => {
                const account = JSON.parse(e.target.dataset.account);
                const { accountManager } = await import('../accountManager.js');
                accountManager.switchAccount(account);
            });
        });
    },

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        document.getElementById('app').prepend(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    },

    showSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.textContent = message;
        document.getElementById('app').prepend(successDiv);
        setTimeout(() => successDiv.remove(), 3000);
    }
};