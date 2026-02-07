import { fetchData } from './api';

/**
 * Fetch an existing blueprint by opportunity ID
 */
export const getBlueprintByOpportunity = async (opportunityId) => {
    try {
        const data = await fetchData(`/blueprints/${opportunityId}`);
        return data;
    } catch (err) {
        console.error('Error fetching blueprint:', err);
        throw err;
    }
};

/**
 * Trigger generation of a new blueprint
 */
export const generateBlueprint = async (opportunityId) => {
    try {
        const data = await fetchData(`/blueprints/${opportunityId}/generate`, {
            method: 'POST'
        });
        return data;
    } catch (err) {
        console.error('Error generating blueprint:', err);
        throw err;
    }
};
