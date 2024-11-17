// Create the map object and set its view to the US
const map = L.map('map').setView([37.8, -96], 4);

// Use a dark tile layer for the map background
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attribution">CARTO</a>',
}).addTo(map);

// Function to set color based on energy demand value
function getColor(d) {
    return d > 1000 ? '#800026' :
           d > 500  ? '#BD0026' :
           d > 200  ? '#E31A1C' :
           d > 100  ? '#FC4E2A' :
           d > 50   ? '#FD8D3C' :
           d > 20   ? '#FEB24C' :
           d > 10   ? '#FED976' :
                      '#FFEDA0';
}

// Function to apply style to each feature (county)
function style(feature) {
    return {
        fillColor: getColor(feature.properties.demand || 0),  // default to 0 if 'demand' not present
        weight: 1,
        opacity: 1,
        color: 'white',
        fillOpacity: 0.7
    };
}

// Adding geoJSON layer for US counties
const geojsonData = {{ geojson_data | safe }};
L.geoJson(geojsonData, {
    style: style
}).addTo(map);