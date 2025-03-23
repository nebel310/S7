// Объект для управления аутентификацией
const Auth = {
    // Проверка авторизации
    checkAuth: async () => {
        const accessToken = localStorage.getItem('access_token');
        const refreshToken = localStorage.getItem('refresh_token');
        
        if (!accessToken && !refreshToken) return false;

        try {
            // Проверка валидности access токена
            await Auth.fetchWithRefresh('/auth/me');
            return true;
        } catch (error) {
            Auth.logout();
            return false;
        }
    },

    // Запрос с автоматическим обновлением токена
    fetchWithRefresh: async (url, options = {}) => {
        try {
            return await fetch(url, {
                ...options,
                headers: {
                    ...options.headers,
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });
        } catch (error) {
            if (error.response?.status === 401) {
                const newToken = await Auth.refreshToken();
                localStorage.setItem('access_token', newToken);
                return fetch(url, options);
            }
            throw error;
        }
    },

    // Обновление токена
    refreshToken: async () => {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) throw new Error('No refresh token');
        
        const response = await fetch(`/auth/refresh?refresh_token=${refreshToken}`);
        const { access_token } = await response.json();
        return access_token;
    },

    // Выход из системы
    logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = 'login.html?success=Вы успешно вышли';
    },

    // Показать сообщение
    showFlash: (message, type = 'error') => {
        const flashDiv = document.getElementById('flashMessage');
        if (!flashDiv) return;
        
        flashDiv.textContent = message;
        flashDiv.className = `flash-message ${type}`;
        flashDiv.style.display = 'block';
        
        setTimeout(() => {
            flashDiv.style.display = 'none';
        }, 5000);
    }
};

// Обработчики форм
document.addEventListener('DOMContentLoaded', () => {
    // Проверка авторизации
    Auth.checkAuth().then(isAuthenticated => {
        if (isAuthenticated && (location.pathname.includes('login') || location.pathname.includes('register'))) {
            window.location.href = 'profile.html';
        }
    });

    // Парсинг параметров URL
    const urlParams = new URLSearchParams(location.search);
    const error = urlParams.get('error');
    const success = urlParams.get('success');
    
    if (error) Auth.showFlash(decodeURIComponent(error), 'error');
    if (success) Auth.showFlash(decodeURIComponent(success), 'success');

    // Очистка параметров из URL
    window.history.replaceState({}, document.title, window.location.pathname);
});

// Форма входа
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        email: e.target.email.value,
        password: e.target.password.value
    };

    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            Auth.showFlash('Успешный вход!', 'success');
            setTimeout(() => window.location.href = 'profile.html', 1500);
        } else {
            throw new Error(data.detail || 'Ошибка авторизации');
        }
    } catch (error) {
        Auth.showFlash(error.message);
    }
});

// Форма регистрации
document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (e.target.password.value !== e.target.password_confirm.value) {
        Auth.showFlash('Пароли не совпадают');
        return;
    }

    const formData = {
        username: e.target.username.value.trim(),
        email: e.target.email.value.trim(),
        password: e.target.password.value,
        password_confirm: e.target.password_confirm.value
    };

    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if (response.ok) {
            window.location.href = `login.html?success=${encodeURIComponent(data.message)}`;
        } else {
            throw new Error(data.detail || 'Ошибка регистрации');
        }
    } catch (error) {
        Auth.showFlash(error.message);
    }
});

// Валидация пароля
document.getElementById('password')?.addEventListener('input', function() {
    const strength = calculatePasswordStrength(this.value);
    const indicator = this.parentElement.querySelector('.password-strength');
    indicator.className = `password-strength ${strength}`;
});

function calculatePasswordStrength(password) {
    const hasLower = /[a-z]/.test(password);
    const hasUpper = /[A-Z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecial = /[!@#$%^&*]/.test(password);
    
    let strength = 0;
    if (password.length >= 8) strength++;
    if (hasLower && hasUpper) strength++;
    if (hasNumber) strength++;
    if (hasSpecial) strength++;
    
    return strength < 2 ? 'weak' : strength < 4 ? 'medium' : 'strong';
}

// Переключение видимости пароля
document.querySelectorAll('.password-toggle').forEach(button => {
    button.addEventListener('click', () => {
        const input = button.previousElementSibling;
        input.type = input.type === 'password' ? 'text' : 'password';
        button.innerHTML = input.type === 'password' 
            ? '<i class="fas fa-eye"></i>' 
            : '<i class="fas fa-eye-slash"></i>';
    });
});