// Agregar estos métodos a la clase Api

async updateActivity(data) {
    const token = await chrome.storage.local.get('token');
    if (!token.token) {
        throw new Error('No authentication token');
    }

    const response = await fetch(`${API_URL}/api/admin/users/${data.userId}/sessions/${data.accountId}`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token.token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            domain: data.domain,
            timestamp: data.timestamp
        })
    });

    if (!response.ok) {
        throw new Error('Failed to update activity');
    }

    return response.json();
}

async endSession(data) {
    const token = await chrome.storage.local.get('token');
    if (!token.token) {
        throw new Error('No authentication token');
    }

    const response = await fetch(
        `${API_URL}/api/admin/users/${data.userId}/sessions/${data.accountId}?domain=${data.domain}`, 
        {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token.token}`
            }
        }
    );

    if (!response.ok) {
        throw new Error('Failed to end session');
    }

    return response.json();
}