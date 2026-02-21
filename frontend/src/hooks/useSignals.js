import { useState, useEffect, useCallback } from 'react';
import { getSignals, acceptSignal as apiAccept, rejectSignal as apiReject } from '../services/signalsService';

export const useSignals = (category = 'All') => {
    const [signals, setSignals] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchSignals = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getSignals(category);
            // After our normalization in services, it should always be { signals: [...] }
            setSignals(result.signals || []);
        } catch (err) {
            setError(err.message || 'Failed to fetch signals');
        } finally {
            setLoading(false);
        }
    }, [category]);

    useEffect(() => {
        fetchSignals();
    }, [fetchSignals]);

    const acceptSignal = useCallback(async (signalId) => {
        try {
            await apiAccept(signalId);
            setSignals(prev =>
                prev.map(s => s.id === signalId ? { ...s, status: 'Accepted' } : s)
            );
        } catch (err) {
            setError(err.message || 'Failed to accept signal');
        }
    }, []);

    const rejectSignal = useCallback(async (signalId) => {
        try {
            await apiReject(signalId);
            setSignals(prev =>
                prev.map(s => s.id === signalId ? { ...s, status: 'Rejected' } : s)
            );
        } catch (err) {
            setError(err.message || 'Failed to reject signal');
        }
    }, []);

    return { signals, loading, error, acceptSignal, rejectSignal, refetch: fetchSignals };
};
