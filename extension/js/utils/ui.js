export const ui = {
    updateAccountsList(accounts, currentAccount) {
        const accountsList = document.getElementById('accounts-list');
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
    },

    showError(message) {
        const errorDiv = document.getElementById('login-error');
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
        setTimeout(() => {
            errorDiv.classList.add('hidden');
        }, 5000);
    },

    updateGlobalSessionInfo(stats) {
        const infoDiv = document.getElementById('global-session-info');
        infoDiv.textContent = `Active sessions: ${stats.total_active_sessions}`;
    },

    // [Previous methods remain unchanged]
};