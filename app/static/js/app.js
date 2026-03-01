const API_BASE = '/api';
let currentSessionId = null;
let eventSource = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    checkAuth();

    // Event Listeners
    if (document.getElementById('login-form')) {
        document.getElementById('login-form').addEventListener('submit', handleLogin);
    }
    if (document.getElementById('register-form')) {
        document.getElementById('register-form').addEventListener('submit', handleRegister);
    }

    // Chat Event Listeners
    const msgInput = document.getElementById('message-input');
    if (msgInput) {
        msgInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        msgInput.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
            const sendBtn = document.getElementById('send-btn');
            sendBtn.disabled = this.value.trim().length === 0;
        });

        document.getElementById('send-btn').addEventListener('click', sendMessage);
        document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
    }
});

// Toast Notification
function showToast(message, type = 'danger') {
    const toastContainer = document.getElementById('toast-container');
    const toastClass = type === 'danger' ? 'bg-danger text-white' : 'bg-success text-white';
    const toastHTML = `
        <div class="toast align-items-center ${toastClass} border-0 show" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    toastContainer.innerHTML += toastHTML;
    setTimeout(() => {
        const toasts = toastContainer.querySelectorAll('.toast');
        if (toasts.length > 0) toasts[0].remove();
    }, 5000);
}

// Authentication
function setAuthToken(token) {
    localStorage.setItem('auth_token', token);
}

function getAuthToken() {
    return localStorage.getItem('auth_token');
}

function logout() {
    localStorage.removeItem('auth_token');
    window.location.href = '/login';
}

async function handleLogin(e) {
    e.preventDefault();
    const btn = document.getElementById('login-btn');
    const spinner = document.getElementById('login-spinner');

    btn.disabled = true;
    spinner.classList.remove('d-none');

    const formData = new URLSearchParams();
    formData.append('username', document.getElementById('username').value);
    formData.append('password', document.getElementById('password').value);

    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });
        const data = await res.json();
        if (res.ok) {
            setAuthToken(data.access_token);
            window.location.href = '/';
        } else {
            showToast(data.detail);
        }
    } catch (err) {
        showToast('Login failed. Server error.');
    } finally {
        btn.disabled = false;
        spinner.classList.add('d-none');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const btn = document.getElementById('register-btn');
    const spinner = document.getElementById('register-spinner');

    btn.disabled = true;
    spinner.classList.remove('d-none');

    const payload = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    try {
        const res = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
            showToast('Registration successful! Please login.', 'success');
            setTimeout(() => window.location.href = '/login', 1500);
        } else {
            showToast(data.detail);
        }
    } catch (err) {
        showToast('Registration failed.');
    } finally {
        btn.disabled = false;
        spinner.classList.add('d-none');
    }
}

async function checkAuth() {
    const token = getAuthToken();
    const isAuthPage = window.location.pathname === '/login' || window.location.pathname === '/register';

    if (!token && !isAuthPage) {
        window.location.href = '/login';
        return;
    }

    if (token) {
        try {
            const res = await fetch(`${API_BASE}/auth/me`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                if (isAuthPage) window.location.href = '/';
                const user = await res.json();
                const userNameEl = document.getElementById('user-profile-name');
                if (userNameEl) userNameEl.textContent = user.username;
                if (!isAuthPage) loadChatSessions(); // Only load sessions if we're on the main app
            } else {
                logout();
            }
        } catch {
            if (!isAuthPage) logout();
        }
    }
}

// Chat Management
async function loadChatSessions() {
    try {
        const res = await fetch(`${API_BASE}/chat/sessions`, {
            headers: { 'Authorization': `Bearer ${getAuthToken()}` }
        });
        const sessions = await res.json();
        const list = document.getElementById('chat-list');
        list.innerHTML = '';

        if (sessions.length === 0) {
            list.innerHTML = `<div class="text-center text-muted mt-5 small">No chats yet.</div>`;
            return;
        }

        sessions.forEach(session => {
            const div = document.createElement('div');
            div.className = `chat-list-item p-2 mb-2 rounded border-start border-3 border-transparent d-flex justify-content-between align-items-center ${session.id === currentSessionId ? 'active text-primary' : 'text-body-secondary'}`;
            div.onclick = () => loadChatHistory(session.id, session.title);
            div.innerHTML = `
                <div class="text-truncate fw-medium small pe-2" style="max-width: 170px;">
                    <i class="bi bi-chat-left-text me-2"></i>${session.title}
                </div>
                <div class="d-flex text-body-tertiary">
                    <i class="bi bi-trash cursor-pointer delete-chat-icon" onclick="event.stopPropagation(); deleteChat(${session.id})" style="font-size: 0.9rem;"></i>
                </div>
            `;
            list.appendChild(div);
        });
    } catch (err) {
        console.error('Failed to view sessions', err);
    }
}

async function newChat() {
    try {
        const res = await fetch(`${API_BASE}/chat/sessions`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title: 'New Chat' })
        });
        const session = await res.json();
        await loadChatSessions();
        await loadChatHistory(session.id, session.title);

        // Hide offcanvas on mobile
        const offcanvas = bootstrap.Offcanvas.getInstance(document.getElementById('sidebarMenu'));
        if (offcanvas) offcanvas.hide();

    } catch (err) {
        showToast('Failed to create new chat.');
    }
}

async function loadChatHistory(sessionId, title) {
    currentSessionId = sessionId;
    document.getElementById('mobile-chat-title').textContent = title;
    const container = document.getElementById('chat-messages');
    container.innerHTML = '<div class="text-center my-4"><div class="spinner-border text-primary"></div></div>';

    // Highlight list
    const items = document.querySelectorAll('.chat-list-item');
    items.forEach(el => el.classList.remove('active', 'text-primary'));

    try {
        const res = await fetch(`${API_BASE}/chat/sessions/${sessionId}`, {
            headers: { 'Authorization': `Bearer ${getAuthToken()}` }
        });
        const session = await res.json();

        container.innerHTML = '';
        if (session.messages.length === 0) {
            container.innerHTML = document.getElementById('welcome-screen').outerHTML; // Preserve design
            return;
        }

        session.messages.forEach(msg => appendMessage(msg.role, msg.content));
        scrollToBottom();
        loadChatSessions(); // refresh active state visually
    } catch (err) {
        container.innerHTML = '<div class="text-center text-danger my-4">Failed to load history.</div>';
    }
}

// Render simple markdown to html
function formatContent(text) {
    if (!text) return text;
    // VERY Basic markdown renderer for codeblocks and paragraphs
    let html = text.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = `<p>${html.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>')}</p>`;
    return html;
}

function appendMessage(role, content) {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    const isUser = role === 'user';
    div.className = `chat-message ${isUser ? 'user' : 'assistant'} shadow-sm d-flex flex-column`;

    // Add Role Label
    const roleLabel = document.createElement('div');
    roleLabel.className = 'd-flex align-items-center mb-1 gap-2 ' + (isUser ? 'text-white-50 flex-row-reverse' : 'text-body-tertiary');
    roleLabel.style.fontSize = '0.75rem';
    roleLabel.innerHTML = isUser ? `<img src="https://ui-avatars.com/api/?name=You&background=random&size=24" class="rounded-circle me-1" alt="User Avatar"> You` : `<img src="https://ui-avatars.com/api/?name=Ollama&background=0D8ABC&color=fff&size=24" class="rounded-circle me-1" alt="Ollama Avatar"> Assistant`;

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.innerHTML = isUser ? content.replace(/\n/g, '<br>') : formatContent(content);

    div.appendChild(roleLabel);
    div.appendChild(textDiv);
    container.appendChild(div);
    return div;
}

function scrollToBottom() {
    const container = document.getElementById('chat-messages');
    container.scrollTop = container.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const stopBtn = document.getElementById('stop-btn');
    const content = input.value.trim();

    if (!content) return;

    // If no session exists, create one first
    if (!currentSessionId) {
        await newChat();
    }

    // Cleanup input
    input.value = '';
    input.style.height = 'auto';
    sendBtn.disabled = true;

    // Update title heuristically for new chats
    const msgs = document.querySelectorAll('.chat-message');
    if (msgs.length === 0) {
        const title = content.split(' ').slice(0, 4).join(' ') + '...';
        await fetch(`${API_BASE}/chat/sessions/${currentSessionId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title: title })
        });
        loadChatSessions();
    }

    appendMessage('user', content);
    scrollToBottom();

    // UI prep for Assistant typing
    const assistantBubble = appendMessage('assistant', '<span class="spinner-grow spinner-grow-sm text-secondary" role="status"></span>');
    const textNode = assistantBubble.querySelector('.message-text');
    scrollToBottom();

    sendBtn.classList.add('d-none');
    stopBtn.classList.remove('d-none');

    // Switch to Fetch API for POST request, capturing the SSE stream response
    try {
        const res = await fetch(`${API_BASE}/chat/sessions/${currentSessionId}/message`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: content, role: 'user' })
        });

        if (!res.ok) {
            if (res.status === 401) logout();
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        // Handle SSE stream manually
        const reader = res.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let botResponseText = "";
        textNode.innerHTML = "";

        // Stop Button Logic
        const abortController = new AbortController();
        stopBtn.onclick = () => {
            abortController.abort();
            reader.cancel();
            resetInputUI();
        };

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });

            const lines = chunk.split('\n');
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = line.slice(6);
                    botResponseText += data;
                    textNode.innerHTML = formatContent(botResponseText);
                    scrollToBottom();
                }
            }
        }
    } catch (err) {
        textNode.innerHTML = `<span class="text-danger">Error: ${err.message}</span>`;
    } finally {
        resetInputUI();
    }
}

function resetInputUI() {
    const sendBtn = document.getElementById('send-btn');
    const stopBtn = document.getElementById('stop-btn');
    sendBtn.classList.remove('d-none');
    stopBtn.classList.add('d-none');
    const input = document.getElementById('message-input');
    sendBtn.disabled = input.value.trim().length === 0;
}

// Delete Chat via Modal
let chatToDelete = null;

function deleteChat(id) {
    chatToDelete = id;
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}

document.getElementById('confirm-delete-btn')?.addEventListener('click', async () => {
    if (!chatToDelete) return;
    try {
        const res = await fetch(`${API_BASE}/chat/sessions/${chatToDelete}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${getAuthToken()}` }
        });
        if (res.ok) {
            if (currentSessionId === chatToDelete) {
                document.getElementById('chat-messages').innerHTML = document.getElementById('welcome-screen').outerHTML;
                currentSessionId = null;
                document.getElementById('mobile-chat-title').textContent = 'New Chat';
            }
            loadChatSessions();
        }
    } catch (err) {
        showToast('Failed to delete chat');
    } finally {
        const modal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
        modal.hide();
        chatToDelete = null;
    }
});

// Theme Management
function initTheme() {
    const storedTheme = localStorage.getItem('theme');
    if (storedTheme) {
        document.documentElement.setAttribute('data-bs-theme', storedTheme);
    } else {
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-bs-theme', prefersDark ? 'dark' : 'light');
    }
    updateThemeUI();
}

function toggleTheme(e) {
    e.preventDefault();
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeUI();
}

function updateThemeUI() {
    const themeBtn = document.getElementById('theme-toggle');
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    if (themeBtn) {
        if (currentTheme === 'dark') {
            themeBtn.innerHTML = '<i class="bi bi-sun"></i> Light Mode';
        } else {
            themeBtn.innerHTML = '<i class="bi bi-moon-stars"></i> Dark Mode';
        }
    }
}
