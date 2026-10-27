from datetime import datetime, timezone  # Help us record when we downloaded the forecast
from pathlib import Path  # Help Python work with folders and files
import requests


url ="https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 51.5074,
    "longitude": -0.1278,
    "hourly" : "temperature_2m,precipitation_probability,wind_speed_10m", 
    "timezone": "Europe/London",
    "forecast_days": 1,

}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

print(response.status_code) 

data = response.json() # Make the weather response easier to work with in Python

print(data.keys())  # Show the names of the main sections we received


print(data["hourly"].keys()) # Show what weather information is available hour by hour

print(data["hourly"]["time"][:3])  # Show the first three times

print(data["hourly"]["temperature_2m"][:3])   # Show the temperatures for those three times 

# Keep new downloads separate from our demonstration sample
raw_folder = Path("data/raw/live")
raw_folder.mkdir(parents=True, exist_ok=True)  # Create the folder if needed

# Record the retrieval time in UTC, including fractions of a second
retrieved_at = datetime.now(timezone.utc)
timestamp = retrieved_at.strftime("%Y%m%dT%H%M%S%fZ")

# Give each download its own filename
raw_file = raw_folder / f"london_forecast_{timestamp}.json"

# Create a new file and save the original response unchanged
with raw_file.open("xb") as file:
    file.write(response.content)

print(f"Saved weather data to {raw_file}")
print(f"Retrieved at: {retrieved_at.isoformat()}")