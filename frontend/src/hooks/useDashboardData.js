import { useState, useEffect } from 'react';
import { getDashboardStats } from '../services/dashboardService';

export const useDashboardData = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getDashboardStats().then(stats => {
            setData(stats);
            setLoading(false);
        });
    }, []);

    return { data, loading };
};
