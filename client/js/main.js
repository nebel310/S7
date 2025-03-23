// Инициализация темы при загрузке
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

// Переключение темы
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Обновление иконки
    const themeIcon = document.querySelector('.theme-toggle i');
    themeIcon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}

// Закрытие модальных окон
function closeModals() {
    document.querySelectorAll('.auth-modal').forEach(modal => {
        modal.classList.remove('active');
    });
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    
    // Закрытие модалок по клику вне области
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('auth-modal')) {
            closeModals();
        }
    });
    
    // Плавное появление элементов
    document.querySelectorAll('[data-animate]').forEach(el => {
        el.style.opacity = '0';
        setTimeout(() => {
            el.style.transition = 'opacity 0.6s ease-out';
            el.style.opacity = '1';
        }, 100);
    });
});

// Общая функция для API запросов
async function makeRequest(url, method, body, auth = false) {
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (auth) {
        const token = localStorage.getItem('access_token');
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(url, {
            method,
            headers,
            body: JSON.stringify(body)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Request failed:', error);
        throw error;
    }
}