export class GroupManager {
    constructor() {
        this.groupSelect = document.getElementById('group-select');
        this.csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    }

    async init() {
        if (this.groupSelect) {
            await this.loadGroups();
            this.attachEventListeners();
        }
    }

    async loadGroups() {
        try {
            const response = await fetch('/admin/api/groups', {
                headers: {
                    'X-CSRFToken': this.csrfToken,
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Failed to load groups');
            }

            const groups = await response.json();
            this.updateGroupSelect(groups);
        } catch (error) {
            console.error('Error loading groups:', error);
        }
    }

    updateGroupSelect(groups) {
        if (!Array.isArray(groups)) {
            console.error('Expected groups to be an array:', groups);
            return;
        }

        this.groupSelect.innerHTML = `
            <option value="">Choose a group...</option>
            ${groups.map(group => `
                <option value="${group.id}">
                    ${group.name} (${group.account_count} accounts)
                </option>
            `).join('')}
        `;
    }

    attachEventListeners() {
        const form = document.getElementById('assign-group-form');
        if (form) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.handleGroupAssignment(e);
            });
        }
    }

    async handleGroupAssignment(event) {
        const groupId = this.groupSelect.value;
        if (!groupId) {
            alert('Please select a group');
            return;
        }

        const userId = document.querySelector('[data-user-id]')?.dataset.userId;
        if (!userId) {
            alert('User ID not found');
            return;
        }

        try {
            const response = await fetch(`/admin/users/${userId}/groups/${groupId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken,
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            if (data.success) {
                location.reload();
            } else {
                alert(data.message || 'Failed to assign group');
            }
        } catch (error) {
            console.error('Error:', error);
            alert(`Error assigning group: ${error.message}`);
        }
    }
}