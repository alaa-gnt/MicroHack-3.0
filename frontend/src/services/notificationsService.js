// Notifications & Alerts data service
import { apiFetch } from './api';

/**
 * Fetch notifications from API.
 */
export const getNotifications = async () => {
    try {
        const response = await apiFetch('/alerts');
        const notifications = response.map(alert => ({
            id: alert.id,
            timeGroup: new Date(alert.created_at).toLocaleDateString(),
            timeDetail: new Date(alert.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            title: alert.title,
            items: [alert.message],
            category: alert.severity || 'Info',
            timestamp: alert.created_at,
            isRead: alert.is_read,
        }));

        return {
            notifications,
            unreadCount: notifications.filter(n => !n.isRead).length
        };
    } catch (error) {
        console.error("Failed to fetch notifications:", error);
        return { notifications: [], unreadCount: 0 };
    }
};

/**
 * Mark a notification as read.
 */
export const markNotificationAsRead = async (notificationId) => {
    try {
        return await apiFetch(`/alerts/${notificationId}/read`, {
            method: 'PATCH'
        });
    } catch (error) {
        console.error("Failed to mark notification as read:", error);
        return { success: false };
    }
};
