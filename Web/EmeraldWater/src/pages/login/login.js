const applyButton = document.getElementById('apply-button');
var passwordToggle = document.getElementById('password-toggle');
passwordToggle._set = false;
const loginInput    = document.getElementById('login');
const passwordInput = document.getElementById('password');
const signUpButton = document.getElementById('to-sign-up');

// Login
function saveToken(token) {

  localStorage.setItem('authToken', token);
}

async function login(username, password) {
  const urlEncodedData = new URLSearchParams({
    'username': username,
    'password': password
  });

  const response = await fetch('http://127.0.0.1:6789/token', {
    method: 'POST',
    headers: {
      'accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: urlEncodedData
  });

  if (response.ok) {
    const data = await response.json();
    saveToken(data.access_token);
    window.location.href = '/';
  } else {
    alert('Login failed');
  }
}

// Go to sign up
signUpButton.onclick = () => {
    window.location.href = '/src/pages/sign-up/sign-up.html';
}

// Send button
applyButton.onclick = () => {
    let result = getCheckValues(loginInput, passwordInput);
    if (result == undefined) return;
    login(result.login, result.password);
}

// Password toggle
passwordToggle.onclick = () => {
    passwordToggle._set = !passwordToggle._set;
    if (passwordToggle._set) {
        passwordToggle.children[0].src = "/public/Password-toggle.svg";
        passwordToggle.children[0].style.left = "4%";
        passwordToggle.children[0].alt = "Oppened password lock";
        passwordInput.type = 'text';
    } else {
        passwordToggle.children[0].src = "/public/Password.svg";
        passwordToggle.children[0].style.left = "0";
        passwordToggle.children[0].alt = "Closed password lock";
        passwordInput.type = 'password';
    }
};

// Inputs: verify and restrict
function loginValidator(object) {
    object.value = object.value.replace(/[^a-zA-Z0-9_\.]/g, '').replace(/\s+/g, '');

    const maxLength = 120;
    if (object.value.length > maxLength) {
      object.value = object.value.substring(0, maxLength);
    }

    object.setCustomValidity('');
    return true;
}

function loginCheckValidate(object) {
    let result = loginValidator(object);
    if (result) {
        object.classList.remove('invalid');
    }
    return result;
}

loginInput.oninput = () => { loginCheckValidate(loginInput); };
loginInput.onblur  = () => { loginCheckValidate(loginInput); };

// ---

function passwordValidator(object) {
    object.value = object.value.replace(/\s+/g, '');
    let found_incorrect = object.value.match(/[^a-zA-Z0-9!@#$%\^&*\(\)\.,]/g, '');
    if (found_incorrect != undefined && found_incorrect.length > 0) {
        found_incorrect = [...new Set(found_incorrect)];
        object.setCustomValidity(`Incorrect symbol(s): [${found_incorrect.join(' ')}]`);
        object.reportValidity();
        object.classList.add('invalid');
        return undefined;
    };

    const maxLength = 120;
    if (object.value.length > maxLength) {
      object.value = object.value.substring(0, maxLength);
    }

    object.setCustomValidity('');
    return true;
}

function passwordCheckValidate(object) {
    let result = passwordValidator(object);
    if (result) {
        object.classList.remove('invalid');
    }
    return result;
}

passwordInput.oninput = () => { passwordCheckValidate(passwordInput); };
passwordInput.onblur  = () => { passwordCheckValidate(passwordInput); };

// ---

function getCheckValues(login, password) {
    let result = loginCheckValidate(login);
    if (result == undefined) return;
    if (!result) {
        login.classList.add('invalid');
        return;
    }

    login.classList.remove('invalid');

    // ---
    result = passwordCheckValidate(password);
    if (result == undefined) return;
    if (!result) {
        password.classList.add('invalid');
    }

    password.classList.remove('invalid');

    // ---
    if (login.value.trim().length == 0) {
        login.setCustomValidity('Field must not be empty');
        login.reportValidity();
        login.classList.add('invalid');
        return;
    }
    if (password.value.trim().length == 0) {
        password.setCustomValidity('Field must not be empty');
        password.reportValidity();
        password.classList.add('invalid');
        return;
    }

    // ---

    return {
        "login":    login.value,
        "password": password.value
    };
}