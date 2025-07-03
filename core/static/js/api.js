// api.js - Handles API requests for dashboard

async function fetchStats() {
    try {
        const [devicesRes, banksRes] = await Promise.all([
            fetch('/api/v1/devices/'),
            fetch('/api/v1/banks/')
        ]);
        const devices = await devicesRes.json();
        const banks = await banksRes.json();
        document.querySelector('#devices-count .stat-value').textContent = devices.length;
        document.querySelector('#banks-count .stat-value').textContent = banks.length;
    } catch (e) {
        // fallback
    }
}

async function fetchRecentActivity() {
    // This would be replaced with a real endpoint for device history
    // For now, just show a placeholder
    const activityDiv = document.getElementById('recent-activity');
    activityDiv.innerHTML = '<p>Recent device activity will appear here.</p>';
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('devices-count')) {
        fetchStats();
        fetchRecentActivity();
    }
});
