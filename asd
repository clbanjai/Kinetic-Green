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
            const response = await fetch('/county_data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const countyData = await response.json();

            // Add each county to the map
            countyData.forEach(function(county) {
                // Placeholder coordinates - you need to replace this with actual lat/lon for each county
                const lat = county.lat;  // Replace with the actual latitude key
                const lon = county.lon;  // Replace with the actual longitude key

                // Get the Total Score for coloring
                const totalScore = county.Total_Score;

                // Add a circle for each county on the map
                const circle = L.circle([lat, lon], {
                    color: getColor(totalScore),
                    fillColor: getColor(totalScore),
                    fillOpacity: 0.7,
                    radius: 20000  // Radius in meters
                }).addTo(map);

                // Set up the click event to update the info panel
                circle.on('click', function () {
                    document.getElementById('countyInfo').innerHTML = `
                        <p><b>County:</b> ${county.County}</p>
                        <p><b>Energy Demand (GWh):</b> ${county.County_Demand_GWh}</p>
                        <p><b>Wait Time Score:</b> ${county.Wait_Time_Score}</p>
                        <p><b>Supply Score:</b> ${county.Supply_Score}</p>
                        <p><b>Solar Score:</b> ${county.Solar_Score}</p>
                        <p><b>Total Score:</b> ${totalScore}</p>
                    `;
                });
            });
        }

        loadCountyData();
    </script>
</body>
</html>