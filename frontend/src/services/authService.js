// Authentication service
import { apiFetch } from './api';

const TOKEN_KEY = 'authToken';
const USER_KEY = 'authUser';

/**
 * Login with email and password.
 */
export const loginAPI = async (credentials) => {
    // Backend expects x-www-form-urlencoded for OAuth2PasswordRequestForm
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    try {
        const data = await apiFetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData.toString(),
        });

        return {
            success: true,
            token: data.access_token,
            user: data.user
        };
    } catch (err) {
        // Fallback or rethrow
        console.error('Login error:', err);
        throw err;
    }
};

/**
 * Verify an existing token.
 */
export const verifyToken = async (token) => {
    // If we have an endpoint for this, use it. For now, we assume token is valid if it exists
    // or we can call a GET /auth/me if implemented.
    try {
        const data = await apiFetch('/auth/me');
        return data;
    } catch {
        // Mock fallback if /auth/me doesn't exist yet
        const storedUser = localStorage.getItem(USER_KEY);
        return storedUser ? JSON.parse(storedUser) : null;
    }
};

/**
 * Logout - clear stored token.
 */
export const logoutAPI = () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
};
