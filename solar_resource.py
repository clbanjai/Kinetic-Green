import os
import requests
import csv
from datetime import datetime, timedelta
import logging
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Replace with your NREL API Key
NREL_API_KEY ="e83mcbAZVeNG27W4fjSvSEIw5eeuYS2UH6XkdbAV"


if not NREL_API_KEY:
    raise ValueError("NREL_API_KEY environment variable is not set")

OUTPUT_FILE = "texas_solar_production.csv"

def initialize_csv(file_name: str):
    """Initialize the CSV file with headers."""
    if not os.path.exists(file_name):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "datetime", "state", "location_name", "latitude",
                "longitude", "ac_output", "solar_radiation", "capacity_factor"
            ])
        logger.info(f"Initialized CSV file: {file_name}")

def fetch_solar_production(state_code: str, latitude: float, longitude: float):
    """Fetch solar production data using PVWatts API with hourly resolution."""
    url = "https://developer.nrel.gov/api/pvwatts/v6.json"
    params = {
        'api_key': NREL_API_KEY,
        'lat': latitude,
        'lon': longitude,
        'system_capacity': 4,
        'azimuth': 180,
        'tilt': 20,
        'array_type': 1,
        'module_type': 1,
        'losses': 14,
        'timeframe': 'hourly'
    }

    try:
        logger.info(f"Fetching data for coordinates: {latitude}, {longitude}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if 'outputs' not in data or 'ac' not in data['outputs']:
            logger.error("Invalid data structure in API response")
            return None

        return {
            "location_name": f"{data['station_info']['city']}, {data['station_info']['state']}",
            "ac_output": data['outputs']['ac'],
            "solar_radiation": data['outputs'].get('solrad_hourly', [0] * 8760),
            "capacity_factor": float(data['outputs'].get('capacity_factor', 0))
        }

    except requests.RequestException as e:
        logger.error(f"API request error: {str(e)}")
        return None

def store_solar_data(state_code: str, latitude: float, longitude: float, data, file_name: str):
    """Store solar production data into a CSV file."""
    if not data:
        logger.error("No data to store.")
        return

    current_date = datetime(datetime.now().year, 1, 1)
    ac_output = data["ac_output"]
    solar_rad = data["solar_radiation"]
    location_name = data["location_name"]

    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        for hour in range(len(ac_output)):
            date_time = current_date + timedelta(hours=hour)
            writer.writerow([
                date_time.strftime("%Y-%m-%d %H:%M:%S"),
                state_code,
                location_name,
                latitude,
                longitude,
                ac_output[hour],
                solar_rad[hour],
                data["capacity_factor"]
            ])

    logger.info(f"Stored data for {location_name}")

def main():
    # Texas locations
    locations = [
        {"name": "Houston", "state": "TX", "lat": 29.7604, "lon": -95.3698},
        {"name": "Dallas", "state": "TX", "lat": 32.7767, "lon": -96.7970},
        {"name": "Austin", "state": "TX", "lat": 30.2672, "lon": -97.7431},
        {"name": "San Antonio", "state": "TX", "lat": 29.4241, "lon": -98.4936}
    ]

    initialize_csv(OUTPUT_FILE)

    for location in locations:
        logger.info(f"\nProcessing data for {location['name']}, {location['state']}")
        solar_data = fetch_solar_production(
            state_code=location["state"],
            latitude=location["lat"],
            longitude=location["lon"]
        )

        if solar_data:
            store_solar_data(
                state_code=location["state"],
                latitude=location["lat"],
                longitude=location["lon"],
                data=solar_data,
                file_name=OUTPUT_FILE
            )

if __name__ == "__main__":
    main()
