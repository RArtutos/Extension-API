// Account groups management
export class AccountGroupManager {
    constructor() {
        this.groupsContainer = document.getElementById('account-groups');
    }

    init() {
        this.attachEventListeners();
    }

    attachEventListeners() {
        // Group creation
        document.getElementById('create-group-btn')?.addEventListener('click', 
            () => this.showCreateGroupModal());

        // Group assignment
        document.querySelectorAll('.assign-to-group').forEach(button => {
            button.addEventListener('click', (e) => this.handleGroupAssignment(e));
        });
    }

    async showCreateGroupModal() {
        const modal = document.getElementById('create-group-modal');
        if (!modal) return;

        const form = modal.querySelector('form');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.createGroup(new FormData(form));
        });

        new bootstrap.Modal(modal).show();
    }

    async createGroup(formData) {
        try {
            const response = await fetch('/api/admin/groups', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: formData.get('name'),
                    description: formData.get('description')
                })
            });

            if (response.ok) {
                window.location.reload();
            } else {
                throw new Error('Failed to create group');
            }
        } catch (error) {
            console.error('Error creating group:', error);
            alert('Failed to create group. Please try again.');
        }
    }

    async handleGroupAssignment(event) {
        const accountId = event.target.dataset.accountId;
        const groupId = event.target.dataset.groupId;

        try {
            const response = await fetch(`/api/admin/accounts/${accountId}/group/${groupId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                window.location.reload();
            } else {
                throw new Error('Failed to assign group');
            }
        } catch (error) {
            console.error('Error assigning group:', error);
            alert('Failed to assign group. Please try again.');
        }
    }
}