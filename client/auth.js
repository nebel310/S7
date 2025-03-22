const auth = {
    API_URL: 'http://127.0.0.1:8000',

    async makeRequest(url, method, body = null, auth = false) {
        const headers = {};
        if (auth) {
            const token = localStorage.getItem('access_token');
            if (token) headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${this.API_URL}${url}`, {
                method,
                headers: body instanceof FormData ? headers : { 'Content-Type': 'application/json', ...headers },
                body: body instanceof FormData ? body : JSON.stringify(body)
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
            document.getElementById('profileSection').style.display = 'block';
            this.showResumePreview();
        } catch (error) {
            this.showMessage(error.message, 'error');
        }
    },

    async handleRegister(e) {
        e.preventDefault();
        const username = document.getElementById('regUsername').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;
        const passwordConfirm = document.getElementById('regPasswordConfirm').value;

        if (password !== passwordConfirm) {
            return this.showMessage('Пароли не совпадают', 'error');
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
            this.showMessage(error.message, 'error');
        }
    },

    async logout() {
        try {
            await this.makeRequest('/auth/logout', 'POST', null, true);
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            this.checkAuth();
            document.getElementById('profileSection').style.display = 'none';
        } catch (error) {
            console.error('Ошибка выхода:', error);
        }
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

    async uploadFile(url, file) {
        const formData = new FormData();
        formData.append('file', file);
        return await this.makeRequest(url, 'POST', formData, true);
    },

    async showResumePreview() {
        try {
            const response = await fetch(`${this.API_URL}/auth/download-resume`, {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
            });

            if (!response.ok) throw new Error('Резюме не найдено');
            
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            
            const preview = document.getElementById('resumePreview');
            preview.innerHTML = `
                <embed src="${url}#toolbar=0&navpanes=0" type="application/pdf">
                <a href="${url}" download="resume.pdf" class="download-button">Скачать</a>
            `;
        } catch (error) {
            this.showMessage(error.message, 'error');
        }
    },

    showPhotoResult(data) {
        const resultBox = document.getElementById('photoResult');
        resultBox.style.display = 'block';
        resultBox.innerHTML = `
            <p>Результат проверки: ${data.result === 1 ? '✅ Подходит' : '❌ Не подходит'}</p>
            <p>Путь к файлу: ${data.photo_path}</p>
        `;
        resultBox.style.background = data.result === 1 ? '#E8FFA3' : '#FFD3D3';
    },

    showMessage(text, type) {
        const message = document.createElement('div');
        message.className = `message ${type}`;
        message.textContent = text;
        document.body.appendChild(message);
        setTimeout(() => message.remove(), 3000);
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
    },

    initFileUploads() {
        document.getElementById('resumeInput').addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;
            
            try {
                await this.uploadFile('/auth/upload-resume', file);
                this.showResumePreview();
                this.showMessage('Резюме успешно загружено!', 'success');
            } catch (error) {
                this.showMessage(error.message, 'error');
            }
        });

        document.getElementById('photoInput').addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            try {
                const result = await this.uploadFile('/auth/upload-photo', file);
                this.showPhotoResult(result);
                this.showMessage('Фото успешно обработано!', 'success');
            } catch (error) {
                this.showMessage(error.message, 'error');
            }
        });
    }
};

// Инициализация
window.onload = () => {
    auth.checkAuth();
    auth.initFileUploads();
    if (auth.checkAuth()) {
        document.getElementById('profileSection').style.display = 'block';
        auth.showResumePreview();
    }
    window.onclick = (event) => {
        if (event.target.className === 'modal') {
            event.target.style.display = 'none';
        }
    }
};

function toggleTheme() {
    document.body.setAttribute('data-theme', 
        document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'
    );
}