// ── API helpers ──────────────────────────────────────────────────
const API = '';

async function apiFetch(endpoint, options = {}) {
  const token = localStorage.getItem('token');
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${API}${endpoint}`, { ...options, headers });

  if (res.status === 401) {
    localStorage.removeItem('token');
    window.location.href = '/login?expired=1';
    return null;
  }

  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || data.message || 'Something went wrong');
  return data;
}

// ── Toast notifications ───────────────────────────────────────────
function showToast(message, type = 'error') {
  const container = document.getElementById('toastContainer');
  if (!container) { alert(message); return; }

  const icons = { success: '✓', error: '✕' };
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${icons[type] || '!'}</span> ${message}`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('removing');
    toast.addEventListener('animationend', () => toast.remove(), { once: true });
  }, 3500);
}

function showError(elementId, message) {
  const el = document.getElementById(elementId);
  if (el) { el.textContent = message; el.style.display = 'block'; }
  else showToast(message, 'error');
}

// ── Skeleton loader helpers ───────────────────────────────────────
function renderSkeletons(containerId, count = 3) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = Array.from({ length: count }).map(() =>
    `<div class="skeleton skeleton-card"></div>`
  ).join('');
}

// ── Navbar ────────────────────────────────────────────────────────
function setupNavbar() {
  const nav = document.getElementById('authNav');
  if (!nav) return;
  const token = localStorage.getItem('token');
  nav.innerHTML = token
    ? `<a href="/dashboard" class="nav-link">Dashboard</a>
       <a href="#" class="btn btn-sm btn-danger" onclick="logout(event)">Logout</a>`
    : `<a href="/login"  class="nav-link">Login</a>
       <a href="/signup" class="btn btn-sm btn-primary">Sign Up</a>`;
}

function logout(e) {
  if (e) e.preventDefault();
  localStorage.removeItem('token');
  window.location.href = '/login';
}

document.addEventListener('DOMContentLoaded', setupNavbar);
