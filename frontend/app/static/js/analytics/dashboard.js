// Analytics dashboard management
export class AnalyticsDashboard {
    constructor() {
        this.charts = new Map();
        this.updateInterval = null;
    }

    init() {
        this.initCharts();
        this.startDataUpdates();
    }

    initCharts() {
        // Sessions chart
        const sessionsCtx = document.getElementById('sessions-chart')?.getContext('2d');
        if (sessionsCtx) {
            this.charts.set('sessions', new Chart(sessionsCtx, {
                type: 'bar',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Active Sessions',
                        data: [],
                        backgroundColor: 'rgba(54, 162, 235, 0.5)'
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            stepSize: 1
                        }
                    }
                }
            }));
        }

        // Activity chart
        const activityCtx = document.getElementById('activity-chart')?.getContext('2d');
        if (activityCtx) {
            this.charts.set('activity', new Chart(activityCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'User Activity',
                        data: [],
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true
                }
            }));
        }
    }

    startDataUpdates() {
        this.updateData();
        this.updateInterval = setInterval(() => this.updateData(), 60000); // Update every minute
    }

    async updateData() {
        try {
            const response = await fetch('/api/admin/analytics');
            const data = await response.json();
            
            this.updateSessionsChart(data.accounts);
            this.updateActivityTable(data.recent_activity);
            this.updateActivityChart(data.hourly_activity);
        } catch (error) {
            console.error('Error updating analytics:', error);
        }
    }

    updateSessionsChart(accounts) {
        const chart = this.charts.get('sessions');
        if (!chart) return;

        chart.data.labels = accounts.map(a => a.name);
        chart.data.datasets[0].data = accounts.map(a => a.active_sessions);
        chart.update();
    }

    updateActivityChart(hourlyData) {
        const chart = this.charts.get('activity');
        if (!chart) return;

        chart.data.labels = hourlyData.map(d => d.hour);
        chart.data.datasets[0].data = hourlyData.map(d => d.count);
        chart.update();
    }

    updateActivityTable(activities) {
        const tbody = document.querySelector('#activity-table tbody');
        if (!tbody) return;

        tbody.innerHTML = activities.map(activity => `
            <tr>
                <td>${activity.user_id}</td>
                <td>${activity.account_id}</td>
                <td>${activity.domain}</td>
                <td>${this.formatTimestamp(activity.timestamp)}</td>
            </tr>
        `).join('');
    }

    formatTimestamp(timestamp) {
        return new Date(timestamp).toLocaleString();
    }

    cleanup() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        this.charts.forEach(chart => chart.destroy());
    }
}