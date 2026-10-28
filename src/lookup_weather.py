from datetime import datetime  # Help Python understand dates and times
from pathlib import Path  # Help Python check whether a file exists
import duckdb

# Ask which weather data the user wants to check
choice = input("Choose weather data: 1 = demonstration sample, 2 = downloaded forecasts: ")

if choice == "1":
    prepared_file = Path("data/processed/hourly_weather.parquet")
elif choice == "2":
    prepared_file = Path("data/processed/latest_weather.parquet")
else:
    print("Please choose 1 or 2.")
    raise SystemExit(1)  # Stop because we need a valid choice

if not prepared_file.is_file():
    print("Prepared weather data is missing. Run: python src/prepare_weather.py")
    raise SystemExit(1)  # Stop and explain what to do next

chosen_time = input("Enter a date and hour (YYYY-MM-DD HH:00:00): ")

try:  # Try to read the entered date and time
    chosen_time = datetime.strptime(chosen_time, "%Y-%m-%d %H:%M:%S")
except ValueError:  # If the entry is not a valid date in this format
    print("Enter a valid date and time, for example: 2026-10-20 20:00:00")
    raise SystemExit(1)  # Stop because the input needs correcting

if chosen_time.minute != 0 or chosen_time.second != 0:  # Check it is an exact hour
    print("Choose an exact hour, such as 20:00:00.")
    raise SystemExit(1)  # Stop rather than silently change the user's time

connection = duckdb.connect()  # Open the database after checking the input

# Read the prepared table and find the user's chosen hour
query = """
SELECT
    forecast_time,
    temperature_c,
    rain_probability_pct
FROM read_parquet(?)
WHERE forecast_time = CAST(? AS TIMESTAMP)
ORDER BY forecast_time;
"""
# Give SQL the chosen file first, then the chosen walking time
result = connection.sql(query, params=[str(prepared_file), chosen_time])
rows = result.fetchall()  # Bring the matching rows into Python

if not rows:  # If no matching rows were found
    print("No forecast found for that time in the saved data.")
else:  # Otherwise, show the forecast
    result.show()

connection.close() # close the connection to the database when finished 
 