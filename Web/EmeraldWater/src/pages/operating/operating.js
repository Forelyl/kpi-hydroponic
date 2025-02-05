import { roundValues, evaluatePercentageInfo, getColorsStatusBars, MAX_TEMPERATURE, MIN_TEMPERATURE, MAX_ACIDITY, MAX_BASE } from '/src/common_scripts/hydroponic_evaluation.js';

const url_params = new URLSearchParams(window.location.search);
const id = url_params.get('element');

const buttonAddWater10        = document.getElementById('button-add-water');
const buttonAddMineral5       = document.getElementById('button-add-mineral');
const buttonAddTemperature1   = document.getElementById('button-add-temperature');
const buttonLowerTemperature1 = document.getElementById('button-lower-temperature');
const buttonAddAcidity_0_25   = document.getElementById('button-add-acidity');
const buttonLowerAcidity_0_25 = document.getElementById('button-lower-acidity');
const buttonAddOxygen5        = document.getElementById('button-add-oxygen');

const buttonReaload           = document.getElementById('button-reload');
const buttonDelete            = document.getElementById('button-delete');

const waterTankBar            = document.getElementById('water-tank-progress-bar');
const mineralTankBar          = document.getElementById('mineral-progress-bar');
const temperatureBar          = document.getElementById('temperature-progress-bar');
const acidityBar              = document.getElementById('acidity-progress-bar');
const oxygenBar               = document.getElementById('oxygen-progress-bar');

var token = undefined;

// --- Get hydroponic ---
var hydroponic;
setHydroponic();

async function setHydroponic() {
  hydroponic = await getHydroponic();
  if (!hydroponic) {
    window.location.href = '/';
  }
  document.title = `EmeraldWater - operating ${hydroponic.name}`;
  updateBars();
}

async function getHydroponic() {
  token = localStorage.getItem('authToken');
  if (!token) {
      console.error('No token found');
      return;
  }
  const result = await fetch(`http://127.0.0.1:6789/api/hydroponic/${id}`, {
      headers: {
        'accept': 'application/json',
        'Authorization': `Bearer ${token}`
      }
  });
  if (!result.ok) {
      console.error('Error fetching hydroponic');
      return;
  }
  return await result.json();
}

// --- Update hydroponic ---
function updateBars() {
  roundValues(hydroponic);
  let info     = evaluatePercentageInfo(hydroponic);
  const colors = getColorsStatusBars(hydroponic, info);

  waterTankBar.setAttribute('value', hydroponic.value_water + "ml");
  waterTankBar.setAttribute('percentage', info.water_percentage);
  waterTankBar.setAttribute('upper-float-text', hydroponic.water_amount + "ml");
  waterTankBar.setAttribute('bg-color', colors.water);

  mineralTankBar.setAttribute('value', hydroponic.value_minerals + "ml");
  mineralTankBar.setAttribute('percentage', info.minerals_percentage);
  mineralTankBar.setAttribute('bg-color', colors.minerals);

  temperatureBar.setAttribute('value', hydroponic.value_temperature_C + "°C");
  temperatureBar.setAttribute('percentage', info.temperature_percentage);
  temperatureBar.setAttribute('bg-color', colors.temperature);

  acidityBar.setAttribute('value', hydroponic.value_acidity_ph);
  acidityBar.setAttribute('percentage', info.acidity_percentage);
  acidityBar.setAttribute('bg-color', colors.acidity);

  oxygenBar.setAttribute('value', hydroponic.value_oxygen + "ml");
  oxygenBar.setAttribute('percentage', info.oxygen_percentage);
  oxygenBar.setAttribute('bg-color', colors.oxygen);
}

// --- Pseudo and database update hydroponic ---
async function add_water() {
  if (hydroponic == undefined) return;
  hydroponic.value_water = Math.min(hydroponic.value_water + hydroponic.water_amount / 10, hydroponic.water_amount);
  updateBars();
  const result = await fetch(`http://127.0.0.1:6789/api/hydroponic/${id}/update/water/add_10_percent`, {
    headers: {
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    method: 'PATCH'
  });
  if (!result.ok) {
    alert("Connection error");
    window.location.href = '/';
  }
}

async function add_mineral() {
  if (hydroponic == undefined) return;
  hydroponic.value_minerals = Math.min(hydroponic.value_minerals + hydroponic.minerals_amount / 20, hydroponic.minerals_amount);
  updateBars();
  const result = await fetch(`http://127.0.0.1:6789/api/hydroponic/${id}/update/minerals/add_5_percent`, {
    headers: {
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    method: 'PATCH'
  });
  if (!result.ok) {
    alert("Connection error");
    window.location.href = '/';
  }
}

async function add_temperature () {
  if (hydroponic == undefined) return;
  hydroponic.value_temperature_C = Math.min(hydroponic.value_temperature_C + 1, MAX_TEMPERATURE);
  updateBars();
  const result = await fetch(`http://127.0.0.1:6789/api/hydroponic/${id}/update/temperature/add_1_celsius`, {
    headers: {
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    method: 'PATCH'
  });
  if (!result.ok) {
    alert("Connection error");
    window.location.href = '/';
  }
}

async function lower_temperature () {
  if (hydroponic == undefined) return;
  hydroponic.value_temperature_C = Math.max(hydroponic.value_temperature_C - 1, MIN_TEMPERATURE);
  updateBars();
  const result = await fetch(`http://127.0.0.1:6789/api/hydroponic/${id}/update/temperature/lower_1_celsius`, {
    headers: {
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    method: 'PATCH'
  });
  if (!result.ok) {
    alert("Connection error");
    window.location.href = '/';
  }
}

async function add_acidity () {
  if (hydroponic == undefined) return;
  hydroponic.value_acidity_ph = Math.max(hydroponic.value_acidity_ph - 0.25, MAX_ACIDITY);
  updateBars();
  const result = await fetch(`http://127.0.0.1:6789/api/hydroponic/${id}/update/acidity/add_0_25`, {
    headers: {
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    method: 'PATCH'
  });
  if (!result.ok) {
    alert("Connection error");
    window.location.href = '/';
  }
}

async function lower_acidity () {
  if (hydroponic == undefined) return;
  hydroponic.value_acidity_ph = Math.min(hydroponic.value_acidity_ph + 0.25, MAX_BASE);
  updateBars();
  const result = await fetch(`http://127.0.0.1:6789/api/hydroponic/${id}/update/acidity/lower_0_25`, {
    headers: {
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    method: 'PATCH'
  });
  if (!result.ok) {
    alert("Connection error");
    window.location.href = '/';
  }
}

async function add_oxygen() {
  if (hydroponic == undefined) return;
  hydroponic.value_oxygen = Math.min(hydroponic.value_oxygen + hydroponic.oxygen_amount / 20, hydroponic.oxygen_amount);
  updateBars();
  const result = await fetch(`http://127.0.0.1:6789/api/hydroponic/${id}/update/oxygen/add_5_percent`, {
    headers: {
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    method: 'PATCH'
  });
  if (!result.ok) {
    alert("Connection error");
    window.location.href = '/';
  }
}

async function reload_func() {
  if (hydroponic == undefined) return;
  const result = await fetch(`http://127.0.0.1:6789/api/hydroponic/reset/${id}`, {
    headers: {
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    method: 'PATCH'
  });
  if (!result.ok) {
    alert("Connection error");
    window.location.href = '/';
  }
  setHydroponic();
}

async function delete_func() {
  if (hydroponic == undefined) return;
  const result = await fetch(`http://127.0.0.1:6789/api/hydroponic/${id}`, {
    headers: {
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    method: 'DELETE'
  });
  if (!result.ok) {
    alert("Connection error");
  }
  window.location.href = '/';
}

// --- Buttons ---
buttonAddWater10.onclick        = add_water;
buttonAddMineral5.onclick       = add_mineral;
buttonAddTemperature1.onclick   = add_temperature;
buttonLowerTemperature1.onclick = lower_temperature;
buttonAddAcidity_0_25.onclick   = add_acidity;
buttonLowerAcidity_0_25.onclick = lower_acidity;
buttonAddOxygen5.onclick        = add_oxygen;

buttonReaload.onclick           = reload_func;
buttonDelete.onclick            = delete_func;


// --- Timed updated ---
setInterval(setHydroponic, 5000);