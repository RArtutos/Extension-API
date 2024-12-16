// Real-time account status management
export class AccountStatusManager {
    constructor() {
        this.updateInterval = null;
        this.statusElements = new Map();
    }

    init() {
        this.attachStatusElements();
        this.startStatusUpdates();
    }

    attachStatusElements() {
        document.querySelectorAll('[data-account-id]').forEach(element => {
            const accountId = element.dataset.accountId;
            this.statusElements.set(accountId, {
                sessions: element.querySelector('.sessions-count'),
                users: element.querySelector('.active-users'),
                status: element.querySelector('.account-status')
            });
        });
    }

    startStatusUpdates() {
        // Update status every 30 seconds
        this.updateInterval = setInterval(() => this.updateAllStatuses(), 30000);
    }

    async updateAllStatuses() {
        try {
            const response = await fetch('/api/accounts/status');
            const accounts = await response.json();
            
            accounts.forEach(account => this.updateAccountStatus(account));
        } catch (error) {
            console.error('Error updating account statuses:', error);
        }
    }

    updateAccountStatus(account) {
        const elements = this.statusElements.get(account.id.toString());
        if (!elements) return;

        // Update sessions count
        elements.sessions.textContent = `${account.active_sessions}/${account.max_concurrent_users}`;

        // Update active users list
        elements.users.innerHTML = this.renderActiveUsers(account.active_users);

        // Update status indicator
        const isAtCapacity = account.active_sessions >= account.max_concurrent_users;
        elements.status.className = `account-status ${isAtCapacity ? 'at-capacity' : 'available'}`;
        elements.status.title = isAtCapacity ? 'At capacity' : 'Available';
    }

    renderActiveUsers(users) {
        if (!users.length) return '<p class="text-muted">No active users</p>';

        return `
            <ul class="list-unstyled mb-0">
                ${users.map(user => `
                    <li class="active-user">
                        <span class="user-email">${user.user_id}</span>
                        <span class="user-activity">
                            ${this.formatLastActivity(user.last_activity)}
                        </span>
                    </li>
                `).join('')}
            </ul>
        `;
    }

    formatLastActivity(timestamp) {
        if (!timestamp) return 'N/A';
        
        const date = new Date(timestamp);
        const now = new Date();
        const diff = Math.floor((now - date) / 1000);

        if (diff < 60) return 'just now';
        if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
        if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
        return date.toLocaleDateString();
    }

    cleanup() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    }
}