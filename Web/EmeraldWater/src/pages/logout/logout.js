const button   = document.getElementById('apply-button');
const username = document.getElementById('account-name');
button.onclick = () => {
    localStorage.removeItem('authToken');
    window.location.href = '/src/pages/login/login.html';
}

document.addEventListener('DOMContentLoaded', loadUsername);

function loadUsername() {
    const token = localStorage.getItem('authToken');
    if (!token) {
        window.location.href = '/src/pages/login/login.html';
    }
    username.innerText = JSON.parse(atob(token.split('.')[1])).sub;
}