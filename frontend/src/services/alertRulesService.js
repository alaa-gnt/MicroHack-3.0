import { apiFetch } from './api';

/**
 * Create a new alert rule.
 */
export const createAlertRule = async (ruleData) => {
    try {
        const payload = {
            name: ruleData.alertName,
            categories: Object.keys(ruleData.categories).filter(
                (key) => ruleData.categories[key] && key !== 'allCategories'
            ),
            minimum_impact_score: ruleData.minimumScores.impact,
            minimum_urgency_score: ruleData.minimumScores.urgency,
            is_active: true
        };

        return await apiFetch('/alert-rules', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
    } catch (err) {
        console.error('Create alert rule failed:', err);
        throw err;
    }
};

/**
 * Get all alert rules.
 */
export const getAlertRules = async () => {
    try {
        return await apiFetch('/alert-rules');
    } catch (err) {
        console.error('Get alert rules failed:', err);
        return [];
    }
};

/**
 * Delete an alert rule.
 */
export const deleteAlertRule = async (ruleId) => {
    try {
        return await apiFetch(`/alert-rules/${ruleId}`, {
            method: 'DELETE'
        });
    } catch (err) {
        console.error('Delete alert rule failed:', err);
        throw err;
    }
};
