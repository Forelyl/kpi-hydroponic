import { roundValues, evaluatePercentageInfo, getColorsStatusBox } from '/src/common_scripts/hydroponic_evaluation.js';


const hydroponicsContainer = document.getElementsByClassName('hydroponics-container')[0];
document.onload = loadHydroponics();
var hydroponicsList = [];


async function loadHydroponics() {
    hydroponicsList = await getHydroponics();
    if (hydroponicsList == undefined) return;
    if (hydroponicsList.length == 0) {
        return;
    }

    for (let i = 0; i < hydroponicsList.length - 1; i++) {
        addHydroponic(hydroponicsList[i], i);
        addLine();
    }
    let last = hydroponicsList.length - 1;
    addHydroponic(hydroponicsList[last], last);
}

// --- Objects resolvers ---

async function getHydroponics() {
    const token = localStorage.getItem('authToken');
    if (!token) {
        console.error('No token found');
        return;
    }

    const result = await fetch('http://127.0.0.1:6789/api/hydroponic/all', {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
        }
    });

    if (!result.ok) {
        console.error('Error fetching hydroponics list');
        return;
    }

    return await result.json();
}

function addHydroponic(hydroponic, index) {
    const percentageInfo    = evaluatePercentageInfo(hydroponic);
    const colors            = getColorsStatusBox(hydroponic, percentageInfo);
    const hydroponicElement = document.createElement('hydroponic-iter');
    roundValues(hydroponic);

    hydroponicElement.setAttribute('name', hydroponic.name);
    hydroponicElement.setAttribute('bg-color-main', colors.main);
    hydroponicElement.setAttribute('bg-color-secondary1', colors.secondary1);
    hydroponicElement.setAttribute('bg-color-secondary2', colors.secondary2);
    hydroponicElement.setAttribute('bg-color-secondary3', colors.secondary3);
    hydroponicElement.setAttribute('bg-color-secondary4', colors.secondary4);


    hydroponicElement.setAttribute('main-value-volume', `${percentageInfo.water_percentage}%`);
    hydroponicElement.setAttribute('main-value-percentage', percentageInfo.water_percentage);
    hydroponicElement.setAttribute('main-sub-value', `${hydroponic.water_amount}ml`);

    hydroponicElement.setAttribute('sub-value1-volume', `${percentageInfo.minerals_percentage}%`);
    hydroponicElement.setAttribute('sub-value1-percentage', percentageInfo.minerals_percentage);

    hydroponicElement.setAttribute('sub-value2-volume', `${hydroponic.value_temperature_C}°C`);
    hydroponicElement.setAttribute('sub-value2-percentage', percentageInfo.temperature_percentage);


    hydroponicElement.setAttribute('sub-value3-volume', `${hydroponic.value_acidity_ph}`);
    hydroponicElement.setAttribute('sub-value3-percentage', percentageInfo.acidity_percentage);


    hydroponicElement.setAttribute('sub-value4-volume', `${percentageInfo.oxygen_percentage}%`);
    hydroponicElement.setAttribute('sub-value4-percentage', percentageInfo.oxygen_percentage);
    hydroponicElement.id = `hydroponic-${index}`;

    setStatus(hydroponicElement, percentageInfo);

    hydroponicElement.setAttribute('link', `/src/pages/operating/operating.html?element=${hydroponic.id}`);

    // ---

    hydroponicsContainer.appendChild(hydroponicElement);
}

function setStatus(hydroponicElement, percentageInfo) {
    let statusCode = "OK";
    let statusText = "everything is fine";
    let statusColor = "green";

    // find problem - order is important (red > orange > yellow)
    if (percentageInfo.water_percentage < 25) {
        statusCode = "Dangerous";
        statusText = "low water level";
        statusColor = "red";
    } else if (Math.abs(percentageInfo.temperature_error_percentage) > 10) {
        statusCode = "Dangerous";
        statusText = "Dangerous temperature";
        statusColor = "red";
    } else if (percentageInfo.oxygen_percentage < 25) {
        statusCode = "Dangerous";
        statusText = "low oxygen";
        statusColor = "red";
    } else if (Math.abs(percentageInfo.acidity_error_percentage) > 5) {
        statusCode = "Problem";
        statusText = "Dangerous acidity";
        statusColor = "orange";
    } else if (percentageInfo.minerals_percentage < 25) {
        statusCode = "Warning";
        statusText = "low minerals level";
        statusColor = "gold";
    }

    hydroponicElement.setAttribute('status-code', statusCode);
    hydroponicElement.setAttribute('status-text', statusText);
    hydroponicElement.setAttribute('status-color', statusColor);
}

function addLine() {
    const lineElement = document.createElement('horizontal-space-line');
    lineElement.setAttribute('len', '70');
    hydroponicsContainer.appendChild(lineElement);
}

// --- Updates ---
setInterval(updateHydroponicsList, 5000);

async function updateHydroponicsList() {
    const token = localStorage.getItem('authToken');
    if (!token) {
        console.error('No token found');
        return;
    }

    let tempHydroponicsList = await getHydroponics();
    if (tempHydroponicsList == undefined) return;
    let updateLen = Math.min(tempHydroponicsList.length, hydroponicsList.length);
    for (let i = 0; i < updateLen; i++) {
        updateHydroponic(i, tempHydroponicsList[i]);
    }

    addRemoveAdditionalHydroponic(hydroponicsList, tempHydroponicsList);
    hydroponicsList = tempHydroponicsList;
}

function updateHydroponic(index, hydroponic) {
    if (index < 0 || index >= hydroponicsList.length) {
        console.error('Index out of bounds');
        return;
    }
    roundValues(hydroponic);
    const percentageInfo    = evaluatePercentageInfo(hydroponic);
    const colors            = getColorsStatusBox(hydroponic, percentageInfo);
    const hydroponicElement = document.getElementById(`hydroponic-${index}`);

    hydroponicElement.setAttribute('name', hydroponic.name);
    hydroponicElement.setAttribute('bg-color-main', colors.main);
    hydroponicElement.setAttribute('bg-color-secondary1', colors.secondary1);
    hydroponicElement.setAttribute('bg-color-secondary2', colors.secondary2);
    hydroponicElement.setAttribute('bg-color-secondary3', colors.secondary3);
    hydroponicElement.setAttribute('bg-color-secondary4', colors.secondary4);


    hydroponicElement.setAttribute('main-value-volume', `${percentageInfo.water_percentage}%`);
    hydroponicElement.setAttribute('main-value-percentage', percentageInfo.water_percentage);
    hydroponicElement.setAttribute('main-sub-value', `${hydroponic.water_amount}ml`);

    hydroponicElement.setAttribute('sub-value1-volume', `${percentageInfo.minerals_percentage}%`);
    hydroponicElement.setAttribute('sub-value1-percentage', percentageInfo.minerals_percentage);

    hydroponicElement.setAttribute('sub-value2-volume', `${hydroponic.value_temperature_C}°C`);
    hydroponicElement.setAttribute('sub-value2-percentage', percentageInfo.temperature_percentage);


    hydroponicElement.setAttribute('sub-value3-volume', `${hydroponic.value_acidity_ph}`);
    hydroponicElement.setAttribute('sub-value3-percentage', percentageInfo.acidity_percentage);

    hydroponicElement.setAttribute('sub-value4-volume', `${percentageInfo.oxygen_percentage}%`);
    hydroponicElement.setAttribute('sub-value4-percentage', percentageInfo.oxygen_percentage);

    setStatus(hydroponicElement, percentageInfo);

    hydroponicElement.setAttribute('link', `/src/pages/operating/operating.html?element=${hydroponic.id}`);
}

function addRemoveAdditionalHydroponic(oldList, newList) {
    if (newList.length == 0) {
        hydroponicsContainer.innerHTML = '';
        return;
    }

    if (oldList.length > newList.length) {
        for (let i = newList.length; i < oldList.length; i++) {
            hydroponicsContainer.lastChild.remove(); // iter
            hydroponicsContainer.lastChild.remove(); // line separator
        }
    } else if (oldList.length < newList.length) {
        for (let i = oldList.length; i < newList.length; i++) {
            if (i != 0) addLine();
            addHydroponic(newList[i], i);
        }
    }
}