import { useState, useEffect, useMemo, useCallback } from 'react';
import { getTechnologyTrends } from '../services/technologyTrendsService';

export const useTechnologyTrends = () => {
    const [rawData, setRawData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchTrends = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getTechnologyTrends();
            setRawData(result);
        } catch (err) {
            setError(err.message || 'Failed to fetch trends data');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchTrends();
    }, [fetchTrends]);

    const data = useMemo(() => {
        if (!rawData?.trends) return [];
        return rawData.trends;
    }, [rawData]);

    return { data, loading, error, refetch: fetchTrends };
};
