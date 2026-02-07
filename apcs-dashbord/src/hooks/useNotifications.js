import { useState, useEffect, useCallback } from 'react';
import {
    getNotifications,
    markNotificationAsRead,
} from '../services/notificationsService';

/**
 * Hook to manage notifications state.
 * Fetches, groups, and provides mutation helpers.
 */
const useNotifications = () => {
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [unreadCount, setUnreadCount] = useState(0);

    const fetchNotifications = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await getNotifications();
            setNotifications(data.notifications || []);
            setUnreadCount(data.unreadCount || 0);
        } catch (err) {
            setError(err.message || 'Failed to load notifications');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchNotifications();
    }, [fetchNotifications]);

    /**
     * Group notifications by their timeGroup field.
     * Returns an array of { label, notifications } objects preserving order.
     */
    const grouped = (() => {
        const map = new Map();
        notifications.forEach((n) => {
            const label = n.timeDetail
                ? `${n.timeGroup}  ${n.timeDetail}`
                : n.timeGroup;
            if (!map.has(label)) map.set(label, []);
            map.get(label).push(n);
        });
        return Array.from(map.entries()).map(([label, items]) => ({
            label,
            notifications: items,
        }));
    })();

    const markAsRead = useCallback(async (id) => {
        await markNotificationAsRead(id);
        setNotifications((prev) =>
            prev.map((n) => (n.id === id ? { ...n, isRead: true } : n))
        );
        setUnreadCount((c) => Math.max(0, c - 1));
    }, []);

    return {
        notifications,
        grouped,
        loading,
        error,
        unreadCount,
        markAsRead,
        refetch: fetchNotifications,
    };
};

export default useNotifications;
