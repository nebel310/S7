const auth = {
    API_URL: 'http://127.0.0.1:8000',

    async makeRequest(url, method, body = null, auth = false) {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (auth) {
            const token = localStorage.getItem('access_token');
            if (token) headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${this.API_URL}${url}`, {
                method,
                headers,
                body: body ? JSON.stringify(body) : null
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Ошибка сервера');
            return data;
        } catch (error) {
            throw error;
        }
    },

    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const data = await this.makeRequest('/auth/login', 'POST', { email, password });
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            this.hideAuthModal();
            this.checkAuth();
        } catch (error) {
            this.showError('loginError', error.message);
        }
    },

    async handleRegister(e) {
        e.preventDefault();
        const username = document.getElementById('regUsername').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;
        const passwordConfirm = document.getElementById('regPasswordConfirm').value;

        if (password !== passwordConfirm) {
            return this.showError('registerError', 'Пароли не совпадают');
        }

        try {
            await this.makeRequest('/auth/register', 'POST', { 
                username, 
                email, 
                password, 
                password_confirm: passwordConfirm 
            });
            await this.handleLogin(e);
        } catch (error) {
            this.showError('registerError', error.message);
        }
    },

    async logout() {
        try {
            await this.makeRequest('/auth/logout', 'POST', null, true);
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            this.checkAuth();
        } catch (error) {
            console.error('Ошибка выхода:', error);
        }
    },

    showError(elementId, message) {
        const errorElement = document.getElementById(elementId);
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        setTimeout(() => errorElement.style.display = 'none', 3000);
    },

    async checkAuth() {
        const token = localStorage.getItem('access_token');
        const userPanel = document.getElementById('userPanel');
        
        if (!token) {
            userPanel.style.display = 'none';
            return;
        }

        try {
            const userData = await this.makeRequest('/auth/me', 'GET', null, true);
            userPanel.style.display = 'flex';
            document.getElementById('username').textContent = userData.username;
            document.getElementById('userAvatar').textContent = userData.username[0].toUpperCase();
        } catch (error) {
            console.error('Ошибка авторизации:', error);
            this.logout();
        }
    },

    switchTab(tabName) {
        document.querySelectorAll('.auth-tab').forEach(tab => tab.classList.remove('active'));
        document.querySelectorAll('.auth-form').forEach(form => form.style.display = 'none');
        
        document.getElementById(`${tabName}Form`).style.display = 'block';
        event.target.classList.add('active');
    },

    showAuthModal() {
        document.getElementById('authModal').style.display = 'flex';
    },

    hideAuthModal() {
        document.getElementById('authModal').style.display = 'none';
    }
};

// Общие функции
function toggleTheme() {
    document.body.setAttribute('data-theme', 
        document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'
    );
}

// Инициализация при загрузке
window.onload = () => {
    auth.checkAuth();
    window.onclick = (event) => {
        if (event.target.className === 'modal') {
            event.target.style.display = 'none';
        }
    }
};