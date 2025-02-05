const url_params = new URLSearchParams(window.location.search);
const id = url_params.get('element');

const inputs_triads = document.querySelectorAll('trio-input');
const apply_button = document.getElementById('apply-button');



// -----------------------------------------------------------

apply_button.onclick = addHydroponic;

async function addHydroponic() {
    if (!checkInputs()) return;
    let input_dict = getInputs();

    const token = localStorage.getItem('authToken');
    if (!token) {
        console.error('No token found');
        return;
    }

    const result = await fetch(`http://127.0.0.1:6789/api/hydroponic/add`, {
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(input_dict),
      method: 'POST'
    });

    if (!result.ok) {
      alert("Connection error");
    }

    window.location.href = '/';
}

function checkInputs() {
    for (let group of inputs_triads) {
        if (!group.checkValid()) return false;
    }
    return true;
}

function getInputs() {
    let result_dict = {};
    for (let group of inputs_triads) {
        let values = group.getValues();
        if (values === null) return null;
        for (let key in values) {
            result_dict[key] = values[key];
        }
    }
    return result_dict;
}