import { apiFetch } from './api';

/**
 * Fetch feasibility study by Opportunity ID.
 * Returns a single study object if found.
 */
export const getFeasibilityByOpportunity = async (opportunityId) => {
    try {
        const data = await apiFetch(`/feasibility-studies/?opportunity_id=${opportunityId}`);
        // The API returns a list, we take the first one or null
        return data.length > 0 ? data[0] : null;
    } catch (err) {
        console.error(`Feasibility fetch for opp ${opportunityId} failed:`, err);
        throw err;
    }
};

/**
 * Fetch feasibility study by its own ID.
 */
export const getFeasibilityById = async (id) => {
    return await apiFetch(`/feasibility/${id}`);
};
