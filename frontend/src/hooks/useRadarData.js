import { useState, useEffect, useMemo, useCallback } from 'react';
import { getRadarData } from '../services/technologyTrendsService';

export const useRadarData = () => {
    const [rawData, setRawData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchRadar = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getRadarData();
            setRawData(result);
        } catch (err) {
            setError(err.message || 'Failed to fetch radar data');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchRadar();
    }, [fetchRadar]);

    const data = useMemo(() => {
        if (!rawData?.radarData) return [];
        return rawData.radarData;
    }, [rawData]);

    return { data, loading, error, refetch: fetchRadar };
};
