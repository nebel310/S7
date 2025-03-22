const API_BASE = 'http://127.0.0.1:8000';

async function handleApiRequest(endpoint, options = {}) {
    try {
        const url = `${API_BASE}${endpoint}`;
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });

        if (response.status === 401) {
            const newToken = await refreshToken();
            if (newToken) {
                options.headers = {
                    ...options.headers,
                    Authorization: `Bearer ${newToken}`
                };
                return handleApiRequest(endpoint, options);
            }
            throw new Error('Требуется авторизация');
        }

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Ошибка запроса');
        }

        return response.json();
    } catch (error) {
        showError(error.message);
        throw error;
    }
}

async function refreshToken() {
    try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) return null;

        const response = await fetch(`${API_BASE}/auth/refresh`, {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${refreshToken}`
            }
        });

        if (!response.ok) throw new Error('Ошибка обновления токена');
        
        const { access_token } = await response.json();
        localStorage.setItem('access_token', access_token);
        return access_token;
    } catch (error) {
        logout();
        return null;
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login.html';
}

function showError(message) {
    const errorContainer = document.createElement('div');
    errorContainer.className = 'error-message';
    errorContainer.textContent = message;
    
    document.body.appendChild(errorContainer);
    setTimeout(() => errorContainer.remove(), 5000);
}