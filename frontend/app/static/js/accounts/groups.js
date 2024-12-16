export class AccountGroupManager {
    constructor() {
        this.groupsContainer = document.getElementById('account-groups');
        this.csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    }

    init() {
        this.attachEventListeners();
    }

    attachEventListeners() {
        document.getElementById('create-group-btn')?.addEventListener('click', 
            () => this.showCreateGroupModal());

        document.querySelectorAll('.assign-to-group').forEach(button => {
            button.addEventListener('click', (e) => this.handleGroupAssignment(e));
        });
    }

    async showCreateGroupModal() {
        const modal = document.getElementById('create-group-modal');
        if (!modal) return;
        
        // Reset form
        const form = document.getElementById('create-group-form');
        if (form) form.reset();
        
        new bootstrap.Modal(modal).show();
    }

    async handleGroupAssignment(event) {
        const accountId = event.target.dataset.accountId;
        const groupId = event.target.dataset.groupId;

        try {
            const response = await fetch(`/groups/api/${groupId}/accounts/${accountId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                }
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Failed to assign group');
            }

            window.location.reload();
        } catch (error) {
            console.error('Error assigning group:', error);
            alert(error.message || 'Failed to assign group. Please try again.');
        }
    }
}