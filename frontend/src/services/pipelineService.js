import { apiFetch } from './api';

/**
 * Fetch pipeline overview (stages + recent projects).
 */
export const getPipelineOverview = async () => {
    try {
        const data = await apiFetch('/pipeline/overview');
        return data;
    } catch (err) {
        console.error('Pipeline overview API failed:', err);
        throw err;
    }
};

/**
 * Fetch projects for a specific pipeline stage.
 */
export const getStageProjects = async (stageId) => {
    try {
        const data = await apiFetch(`/pipeline/stages/${stageId}/projects`);
        return data.projects || [];
    } catch (err) {
        console.error(`Pipeline stage ${stageId} API failed:`, err);
        return [];
    }
};
