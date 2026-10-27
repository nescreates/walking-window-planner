from pathlib import Path  # Help Python create folders
import duckdb
from inspect_weather import validate_weather  # Reuse our data checks


# Check the original data before preparing it
validate_weather("data/raw/london_sample.json")

# Create a folder for the prepared data
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

connection = duckdb.connect()  # Open DuckDB to run our SQL

# Turn the separate weather lists into rows and save the result
connection.execute("""
    COPY (
        SELECT
            CAST(unnest(hourly.time) AS TIMESTAMP) AS forecast_time,
            unnest(hourly.temperature_2m) AS temperature_c,
            unnest(hourly.precipitation_probability) AS rain_probability_pct
        FROM read_json_auto('data/raw/london_sample.json')
        ORDER BY forecast_time
    )
    TO 'data/processed/hourly_weather.parquet'
    (FORMAT PARQUET);
""")

# Read the saved table to check how many rows it contains
connection.sql("""
    SELECT COUNT(*) AS saved_rows
    FROM read_parquet('data/processed/hourly_weather.parquet')
""").show()

connection.close()  # Close the database connection

print("Saved prepared weather to data/processed/hourly_weather.parquet")
