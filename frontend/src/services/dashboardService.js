// Dashboard data service
import { fetchData } from './api';

export const getDashboardStats = () => {
    return fetchData('/dashboard/stats');
};
