// Declare it in a global scope
var authInterval;

function startAuthCheck() {
    const token     = localStorage.getItem('authToken');
    const wait_time = 60 * 1000; // 60 seconds
    const login_url = '/src/pages/login/login.html'

    // Token expired or missing
    if (!token || isTokenInvalid(token)) window.location.href = login_url;

    // Clear previous interval if it exists
    if (authInterval) clearInterval(authInterval);

    // Token is valid, check periodically
    authInterval = setInterval(() => {
        if (isTokenInvalid(token)) window.location.href = login_url;
    }, wait_time);
}

function isTokenInvalid(token) {
    const payload = JSON.parse(atob(token.split('.')[1])); // Decode JWT
    return payload.exp * 1000 < Date.now();
}

document.addEventListener('DOMContentLoaded', startAuthCheck);