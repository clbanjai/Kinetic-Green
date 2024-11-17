<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>County-Level Energy Demand Map</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.3/leaflet.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.3/leaflet.js"></script>
    <style>
        body {
            margin: 0;
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
        }

        #map {
            height: 100vh;
            width: 100%;
        }

        #infoPanel {
            position: fixed;
            top: 0;
            right: 0px;
            width: 300px;
            height: 100vh;
            background: black;
            color: white;
            box-shadow: -2px 0 5px rgba(0, 0, 0, 0.5);
            padding: 20px;
            transition: right 0.3s ease;
            overflow-y: auto;
            z-index: 1000;
        }

        #infoPanel h2 {
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div id="map"></div>
    <div id="infoPanel">
        <h2>County Information</h2>
        <div id="countyInfo">
            <p><b>County:</b> Select a county to see details.</p>
            <p><b>Energy Demand (GWh):</b></p>
            <p><b>Wait Time Score:</b></p>
            <p><b>Supply Score:</b></p>
            <p><b>Solar Score:</b></p>
            <p><b>Total Score:</b></p>
        </div>
    </div>

    <script>
        // Create the map object and set its view to encompass Texas
        const map = L.map('map').setView([31.9686, -99.9018], 6);

        // Use a dark tile layer for the map background
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: 'Map data &copy; OpenStreetMap contributors &copy; CARTO',
            opacity: 1
        }).addTo(map);

        // Function to set color based on Total Score
        function getColor(score) {
            return score > 8 ? '#006837' :
                   score > 6 ? '#31a354' :
                   score > 4 ? '#78c679' :
                   score > 2 ? '#c2e699' :
                               '#ffffcc';
        }

        // Load county data from Flask endpoint
        async function loadCountyData() {
            try {
                const response = await fetch('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();

                const county = {
                "type": "FeatureCollection",
                "features": data.features.filter(feature => selectedStates.includes(feature.properties.STATE))
                };
                // Add each county to the map
                const geoJsonLayer = L.geoJson(county, {
                style: function (county) {
                    return {
                        fillColor: getColor(county.Total_Score),
                        weight: 1,
                        opacity: 1,
                        color: 'white',
                        fillOpacity: 0.7
                    };
                },
                onEachFeature: function (feature, layer) {
                    layer.on({
                        mouseover: function (e) {
                            e.target.setStyle({
                                weight: 3,
                                color: '#666',
                                fillOpacity: 0.9
                            });
                        },
                        mouseout: function (e) {
                            geoJsonLayer.resetStyle(e.target);
                        },
                        click: function (e) {

                            document.getElementById('countyInfo').innerHTML = `
                            <p><b>County:</b> ${county.County}</p>
                            <p><b>Energy Demand (GWh):</b> ${county.County_Demand_GWh}</p>
                            <p><b>Wait Time Score:</b> ${county.Wait_Time_Score}</p>
                            <p><b>Supply Score:</b> ${county.Supply_Score}</p>
                            <p><b>Solar Score:</b> ${county.Solar_Score}</p>
                            <p><b>Total Score:</b> ${county.Total_Score}</p>
                        `;
                        }
                    });
                }
            }).addTo(map);
            } catch (error) {
                console.error('Error loading county data:', error);
            }
        }

        // Load the data to create the map
        loadCountyData();
    </script>
</body>
</html>
