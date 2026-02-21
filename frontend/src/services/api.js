const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Export for compatibility with existing services
export const API_BASE_URL = API_URL;

// Generic fetch wrapper to handle common API tasks like headers and error checks.
export const apiFetch = async (endpoint, options = {}) => {
  const url = `${API_URL}${endpoint}`;
  const token = localStorage.getItem('authToken');

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout

  const defaultHeaders = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
  };

  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
    signal: controller.signal,
  };

  try {
    const response = await fetch(url, config);
    clearTimeout(timeoutId);

    if (response.status === 401) {
      console.warn('Unauthorized access - maybe redirect to login?');
    }

    if (!response.ok) {
      const errorBody = await response.text();
      throw new Error(`API Error: ${response.status} ${response.statusText} - ${errorBody}`);
    }

    if (response.status === 204) {
      return null;
    }

    return await response.json();
  } catch (error) {
    if (error.name === 'AbortError') {
      console.error('API Request Timed Out (10s)');
    } else {
      console.error('API Request Failed:', error);
    }
    throw error;
  }
};

// Alias for compatibility with existing services
export const fetchData = apiFetch;

export const api = {
  get: (endpoint) => apiFetch(endpoint, { method: 'GET' }),
  post: (endpoint, body) => apiFetch(endpoint, { method: 'POST', body: JSON.stringify(body) }),
  put: (endpoint, body) => apiFetch(endpoint, { method: 'PUT', body: JSON.stringify(body) }),
  delete: (endpoint) => apiFetch(endpoint, { method: 'DELETE' }),
};

