export const MAX_TEMPERATURE = 25;
export const MIN_TEMPERATURE = 5;
const TEMPERATURE_GAP        = MAX_TEMPERATURE - MIN_TEMPERATURE;
const TEMPERATURE_MEDIAN     = (MAX_TEMPERATURE + MIN_TEMPERATURE) / 2;

export const MAX_ACIDITY = 0;
export const MAX_BASE    = 14;
const ACIDITY_GAP        = MAX_ACIDITY - MAX_BASE;
const ACIDITY_MEDIAN     = (MAX_ACIDITY + MAX_BASE) / 2;

export function roundValues(hydroponic) {
    const ROUND_FACTOR = 100.0;
    hydroponic.value_temperature_C = Math.round(hydroponic.value_temperature_C * ROUND_FACTOR) / ROUND_FACTOR;
    hydroponic.value_acidity_ph    = Math.round(hydroponic.value_acidity_ph    * ROUND_FACTOR) / ROUND_FACTOR;
    hydroponic.value_water         = Math.round(hydroponic.value_water         * ROUND_FACTOR) / ROUND_FACTOR;
    hydroponic.value_minerals      = Math.round(hydroponic.value_minerals      * ROUND_FACTOR) / ROUND_FACTOR;
    hydroponic.value_oxygen        = Math.round(hydroponic.value_oxygen        * ROUND_FACTOR) / ROUND_FACTOR;
}

export function evaluatePercentageInfo(hydroponic) {
    const water_percentage = hydroponic.value_water / hydroponic.water_amount * 100.0;
    const minerals_percentage = hydroponic.value_minerals / hydroponic.minerals_amount * 100.0;
    const temperature_percentage = 50.0 + ((hydroponic.value_temperature_C - TEMPERATURE_MEDIAN) / TEMPERATURE_GAP * 100.0);
    const temperature_error_percentage = (hydroponic.value_temperature_C - hydroponic.temperature_C_optimal) / TEMPERATURE_GAP * 100.0;
    const acidity_percentage = 50.0 - ((hydroponic.value_acidity_ph - ACIDITY_MEDIAN) / ACIDITY_GAP * 100.0);
    const acidity_error_percentage = (hydroponic.value_acidity_ph - hydroponic.acidity_optimal_ph) / ACIDITY_GAP * 100.0;
    const oxygen_percentage = hydroponic.value_oxygen / hydroponic.oxygen_amount * 100.0;

    const ROUND_FACTOR = 100.0;
    return {
        "water_percentage":             Math.round(water_percentage       * ROUND_FACTOR) / ROUND_FACTOR,
        "minerals_percentage":          Math.round(minerals_percentage    * ROUND_FACTOR) / ROUND_FACTOR,
        "temperature_percentage":       Math.round(temperature_percentage * ROUND_FACTOR) / ROUND_FACTOR,
        "temperature_error_percentage": Math.round(temperature_error_percentage * ROUND_FACTOR) / ROUND_FACTOR,
        "acidity_percentage":           Math.round(acidity_percentage     * ROUND_FACTOR) / ROUND_FACTOR,
        "acidity_error_percentage":     Math.round(acidity_error_percentage * ROUND_FACTOR) / ROUND_FACTOR,
        "oxygen_percentage":            Math.round(oxygen_percentage      * ROUND_FACTOR) / ROUND_FACTOR,
    };

}

export function getColorsStatusBox(hydroponic, percentageInfo) {
    // placeholder
    const colors = {
        'main':       getWaterColor(hydroponic, percentageInfo),
        'secondary1': getMineralColor(hydroponic, percentageInfo),
        'secondary2': getTemperatureColor(hydroponic, percentageInfo),
        'secondary3': getAcidnessColor(hydroponic, percentageInfo),
        'secondary4': getOxygenColor(hydroponic, percentageInfo),
    };
    return colors;
}

export function getColorsStatusBars(hydroponic, percentageInfo) {
    // placeholder
    const colors = {
        'water':        getWaterColor(hydroponic, percentageInfo),
        'minerals':     getMineralColor(hydroponic, percentageInfo),
        'temperature':  getTemperatureColor(hydroponic, percentageInfo),
        'acidity':      getAcidnessColor(hydroponic, percentageInfo),
        'oxygen':       getOxygenColor(hydroponic, percentageInfo)
    };
    return colors;
}
// "#24d539"

// --- Colors status box ---

/*
Oxygen
#9e336a
#c938c6
#e352e1
#ec73ff

Acidness
#f5ffa9
less:
#91ff61
#55fe0c
More:
#fb9542
#ff790b

Temperature
#66cc6d
less:
#83c4de
#1c3eba
More:
#f1952b
#dd1919

Water
#db7b6f
#70c6e5
#25abdb
#5cd4ff

Mineral
#b71500
#be4141
#c46666
#f68686
*/

function getWaterColor(hydroponic, percentageInfo) {
    const water_percentage = percentageInfo.water_percentage;
    if (water_percentage < 25) return "#db7b6f";
    if (water_percentage < 50) return "#70c6e5";
    if (water_percentage < 75) return "#25abdb";
    return "#5cd4ff"; // >= 75
}

function getMineralColor(hydroponic, percentageInfo) {
    const minerals_percentage = percentageInfo.minerals_percentage;
    if (minerals_percentage < 25) return "#b71500";
    if (minerals_percentage < 50) return "#be4141";
    if (minerals_percentage < 75) return "#c46666";
    return "#f68686"; // >= 75
}

function getTemperatureColor(hydroponic, percentageInfo) {
    let   error   = percentageInfo.temperature_error_percentage;
    const is_cold = error < 0;
    error = Math.abs(error);

    if (error < 10) return "#66cc6d";

    if (is_cold) {
        if (error < 60) return "#83c4de";
        return "#1c3eba"; // >= 60
    }

    // is_hot
    if (error < 60) return "#f1952b";
    return "#dd1919"; // >= 60
}

function getAcidnessColor(hydroponic, percentageInfo) {
    let   error   = percentageInfo.acidity_error_percentage;
    const is_acid = error < 0;
    error = Math.abs(error);
    if (error < 5) return "#f5ffa9";

    if (is_acid) {
        if (error < 60) return "#91ff61";
        return "#55fe0c"; // >= 60
    }

    // is_base
    if (error < 60) return "#fb9542";
    return "#ff790b"; // >= 60

}

function getOxygenColor(hydroponic, percentageInfo) {
    const oxygen_percentage = percentageInfo.oxygen_percentage;
    if (oxygen_percentage < 25) return "#9e336a";
    if (oxygen_percentage < 50) return "#c938c6";
    if (oxygen_percentage < 75) return "#e352e1";
    return "#ec73ff"; // >= 75
}