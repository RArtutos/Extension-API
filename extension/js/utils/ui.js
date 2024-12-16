class UI {
    showLoginForm() {
        document.getElementById('login-form').classList.remove('hidden');
        document.getElementById('account-manager').classList.add('hidden');
    }

    showAccountManager() {
        document.getElementById('login-form').classList.add('hidden');
        document.getElementById('account-manager').classList.remove('hidden');
    }

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
                            ${account.active_sessions}/${account.max_concurrent_users} users
                        </div>
                        ${account.active_users.length > 0 ? `
                            <div class="active-users">
                                <small>Active users:</small>
                                <ul class="user-list">
                                    ${account.active_users.map(user => `
                                        <li>${user.user_id} 
                                            (${this._formatLastActivity(user.last_activity)})
                                        </li>
                                    `).join('')}
                                </ul>
                            </div>
                        ` : ''}
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

    updateAccountStatus(status) {
        const accountItem = document.querySelector('.account-item.active');
        if (accountItem) {
            const sessionInfo = accountItem.querySelector('.session-info');
            sessionInfo.textContent = `${status.active_sessions}/${status.max_concurrent_users} users`;

            const activeUsers = accountItem.querySelector('.active-users');
            if (activeUsers) {
                activeUsers.innerHTML = status.active_users.length > 0 ? `
                    <small>Active users:</small>
                    <ul class="user-list">
                        ${status.active_users.map(user => `
                            <li>${user.user_id} 
                                (${this._formatLastActivity(user.last_activity)})
                            </li>
                        `).join('')}
                    </ul>
                ` : '';
            }
        }
    }

    _formatLastActivity(timestamp) {
        if (!timestamp) return 'N/A';
        
        const date = new Date(timestamp);
        const now = new Date();
        const diff = Math.floor((now - date) / 1000); // difference in seconds

        if (diff < 60) return 'just now';
        if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
        if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
        return date.toLocaleDateString();
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
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        document.getElementById('app').prepend(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }

    showSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.textContent = message;
        document.getElementById('app').prepend(successDiv);
        setTimeout(() => successDiv.remove(), 3000);
    }
}

export const ui = new UI();