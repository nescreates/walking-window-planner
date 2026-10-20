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

raw_folder = Path("data/raw")  # Choose where to keep the original weather response
raw_folder.mkdir(parents=True, exist_ok=True)  # Create the folder if it is missing

raw_file = raw_folder / "london_sample.json"  # Choose the file name

raw_file.write_bytes(response.content)  # Save the response without changing its contents

print(f"Saved weather data to {raw_file}")  # Show where the file was saved