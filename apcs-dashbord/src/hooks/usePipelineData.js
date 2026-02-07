import { useState, useEffect, useCallback } from 'react';
import { getPipelineOverview, getStageProjects } from '../services/pipelineService';

const usePipelineData = () => {
    const [stages, setStages] = useState([]);
    const [recentProjects, setRecentProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchOverview = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await getPipelineOverview();
            setStages(data.stages || []);
            setRecentProjects(data.recentProjects || []);
        } catch {
            setError('Failed to load pipeline data');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchOverview();
    }, [fetchOverview]);

    const fetchStageProjects = useCallback(async (stageId) => {
        try {
            const data = await getStageProjects(stageId);
            return data.projects || [];
        } catch {
            return [];
        }
    }, []);

    return {
        stages,
        recentProjects,
        loading,
        error,
        refetch: fetchOverview,
        fetchStageProjects,
    };
};

export default usePipelineData;
