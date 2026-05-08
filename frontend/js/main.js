// Global Configuration
const API_BASE_URL = 'http://3.6.39.67:5000';

/**
 * Perform a generic fetch wrapper to easily extract JSON and handle errors.
 */
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || data.error || 'API Request Failed');
        }

        return { success: true, data };
    } catch (error) {
        console.error('API Error:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Display an alert message in a specified container
 */
function showAlert(containerId, message, type = 'error') {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.textContent = message;
    container.className = `alert ${type}`;

    // Auto clear after 5s
    setTimeout(() => {
        container.className = 'alert';
        container.textContent = '';
    }, 5000);
}

/**
 * Check if the user is authenticated and redirect if not.
 * @param {string} requiredRole - If defined, ensures user has specific role or bounces them to home.
 */
function requireAuth(requiredRole = null) {
    const userId = localStorage.getItem('user_id');
    const role = localStorage.getItem('role');

    if (!userId) {
        window.location.href = 'login.html';
        return;
    }

    if (requiredRole && role !== requiredRole) {
        window.location.href = 'home.html';
    }
}

/**
 * Logout the user
 */
function logout() {
    localStorage.removeItem('user_id');
    localStorage.removeItem('role');
    localStorage.removeItem('user_name');
    localStorage.removeItem('ticket_id');
    window.location.href = 'login.html';
}

// Global script execution
document.addEventListener('DOMContentLoaded', () => {
    // Add logout hook to navbar if needed
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }

    // Update dynamic UI based on auth state
    const userId = localStorage.getItem('user_id');
    const role = localStorage.getItem('role');
    let userName = localStorage.getItem('user_name');

    const navAuth = document.getElementById('nav-auth');
    if (navAuth && userId) {
        const updateNav = (name) => {
            const profileHTML = `<li style="display: flex; align-items: center; gap: 0.5rem; color: var(--primary-color); font-weight: 600; margin-right: 1rem;"><svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg> ${name}</li>`;

            if (role === 'admin') {
                navAuth.innerHTML = `
                    ${profileHTML}
                    <li><a href="home.html">Home</a></li>
                    <li><a href="admin_dashboard.html">Dashboard</a></li>
                    <li><a href="#" id="logout-btn">Logout</a></li>
                `;
            } else {
                navAuth.innerHTML = `
                    ${profileHTML}
                    <li><a href="home.html">Home</a></li>
                    <li><a href="event_details.html">Event Details</a></li>
                    <li><a href="my_bookings.html">My Bookings</a></li>
                    <li><a href="#" id="logout-btn">Logout</a></li>
                `;
            }

            document.getElementById('logout-btn')?.addEventListener('click', (e) => {
                e.preventDefault();
                logout();
            });
        };

        if (!userName || userName === 'undefined' || userName === 'null') {
            updateNav('Loading...');
            fetchAPI(`/user/${userId}`).then(res => {
                if (res.success && res.data && res.data.name) {
                    localStorage.setItem('user_name', res.data.name);
                    updateNav(res.data.name);
                } else {
                    updateNav('User');
                }
            });
        } else {
            updateNav(userName);
        }
    }
});

/**
 * Format a raw date string into a clean readable date
 */
function formatDate(dateString) {
    if (!dateString) return 'TBD';
    const d = new Date(dateString);
    if (isNaN(d.getTime())) return dateString;
    return d.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}
