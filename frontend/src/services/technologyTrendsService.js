// Technology Trends data service
import { API_BASE_URL, fetchData } from './api';

// Mock data for development — replace with API calls when backend is ready
const MOCK_TRENDS_DATA = {
    trends: [
        { week: 'week 1', ai: 25, blockchain: 15 },
        { week: 'week2', ai: 85, blockchain: 40 },
        { week: 'week 3', ai: 19, blockchain: 55 },
        { week: 'week 3', ai: 4, blockchain: 0 },
        { week: 'week 4', ai: 20, blockchain: 60 },
        { week: 'week 5', ai: 50, blockchain: 35 },
        { week: 'week 6', ai: 10, blockchain: 72 },
        { week: 'week 7', ai: 75, blockchain: 55 },
        { week: 'week 8', ai: 90, blockchain: 90 },
    ]
};

const MOCK_RADAR_DATA = {
    radarData: [
        { name: 'Research', value: 30 },
        { name: 'Development', value: 30 },
        { name: 'Deployment', value: 50 },
        { name: 'Demo', value: 65 },
    ]
};

/**
 * Fetch technology trends data from API.
 */
export const getTechnologyTrends = async () => {
    try {
        const data = await fetchData('/analytics/dashboard');
        const trends = data.trends || [];

        // Group by snapshot_date (or week)
        // For simplicity, we'll map dates to a "Week X" label or just the date
        const grouped = trends.reduce((acc, curr) => {
            const dateStr = new Date(curr.snapshot_date).toLocaleDateString();
            if (!acc[dateStr]) acc[dateStr] = { week: dateStr };
            acc[dateStr][curr.domain_name.toLowerCase()] = curr.signal_count * 10; // Scaling for visualization
            return acc;
        }, {});

        return {
            trends: Object.values(grouped).sort((a, b) => new Date(a.week) - new Date(b.week))
        };
    } catch (err) {
        console.warn('Trends API failed, using mock:', err);
        return MOCK_TRENDS_DATA;
    }
};

/**
 * Fetch radar chart data from API.
 */
export const getRadarData = async () => {
    try {
        const data = await fetchData('/analytics/dashboard');
        const radar = data.tech_radar || [];

        return {
            radarData: radar.map(r => ({
                name: r.tech_name,
                value: r.avg_trl_level * 10 // Map TRL 1-9 to 0-100 approx
            }))
        };
    } catch (err) {
        console.warn('Radar API failed, using mock:', err);
        return MOCK_RADAR_DATA;
    }
};
