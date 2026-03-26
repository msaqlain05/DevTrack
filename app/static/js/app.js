// API Configuration
const API_URL = ''; // Relative to origin

// Setup Authorization Navbar
function setupNavbar() {
    const nav = document.getElementById('authNav');
    if (!nav) return;
    
    const token = localStorage.getItem('token');
    
    if (token) {
        nav.innerHTML = `
            <a href="/dashboard" class="nav-link">Dashboard</a>
            <a href="#" class="btn btn-danger" onclick="logout(event)">Logout</a>
        `;
    } else {
        nav.innerHTML = `
            <a href="/login" class="nav-link">Login</a>
            <a href="/signup" class="btn btn-primary">Sign Up</a>
        `;
    }
}

// Global Logout Utility
function logout(e) {
    if(e) e.preventDefault();
    localStorage.removeItem('token');
    window.location.href = "/login";
}

// Wrapper around Fetch API that handles auth headers natively
async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers
    };

    try {
        const response = await fetch(`${API_URL}${endpoint}`, config);
        
        // Handle 401 Unauthorized globally
        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = "/login?expired=1";
            return null;
        }

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(data.detail || data.message || 'An error occurred');
        }

        return data;
    } catch (error) {
        throw error;
    }
}

// Display error alert utility
function showError(elementId, message) {
    const el = document.getElementById(elementId);
    if(el) {
        el.textContent = message;
        el.style.display = 'block';
    } else {
        alert(message);
    }
}

// Initialize layout globals when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    setupNavbar();
});
