from pathlib import Path  # Help Python create folders
import duckdb
from inspect_weather import validate_weather  # Reuse our data checks
from datetime import datetime, timezone  # Help Python understand retrieval times

# Find our timestamped London forecast downloads
snapshot_files = sorted(
    Path("data/raw/live").glob("london_forecast_*.json")
)

for snapshot_file in snapshot_files:
    # Take the timestamp out of the filename
    timestamp_text = snapshot_file.stem.removeprefix("london_forecast_")

    # Turn that text into a date and time, labelled as UTC
    retrieved_at = datetime.strptime(
        timestamp_text, "%Y%m%dT%H%M%S%fZ"
    ).replace(tzinfo=timezone.utc)

    # Check each download before we use it
    validate_weather(snapshot_file)

    print(f"Checked snapshot: {snapshot_file.name}")
    print(f"Retrieved at: {retrieved_at.isoformat()}")

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
if snapshot_files:  # Only build this output when downloads exist
    # Create an empty table to hold every downloaded forecast hour
    connection.execute("""
        CREATE TABLE hourly_snapshots (
            location VARCHAR,
            forecast_time TIMESTAMP,
            temperature_c DOUBLE,
            rain_probability_pct DOUBLE,
            retrieved_at TIMESTAMPTZ,
            source_file VARCHAR
        )
    """)

    for snapshot_file in snapshot_files:
        # Read the download time from this file's name
        timestamp_text = snapshot_file.stem.removeprefix("london_forecast_")
        retrieved_at = datetime.strptime(
            timestamp_text, "%Y%m%dT%H%M%S%fZ"
        ).replace(tzinfo=timezone.utc)

        # Turn this download into rows and attach its source information
        connection.execute("""
            INSERT INTO hourly_snapshots
            SELECT
                'London' AS location,
                CAST(unnest(hourly.time) AS TIMESTAMP) AS forecast_time,
                unnest(hourly.temperature_2m) AS temperature_c,
                unnest(hourly.precipitation_probability) AS rain_probability_pct,
                CAST(? AS TIMESTAMPTZ) AS retrieved_at,
                CAST(? AS VARCHAR) AS source_file
            FROM read_json_auto(?)
        """, [retrieved_at, str(snapshot_file), str(snapshot_file)])

    # Rank downloads for each London forecast hour: newest first
    connection.execute("""
        CREATE TABLE latest_weather AS
        SELECT * EXCLUDE (snapshot_rank)
        FROM (
            SELECT
                *,
                ROW_NUMBER() OVER (
                    PARTITION BY location, forecast_time
                    ORDER BY retrieved_at DESC, source_file DESC
                ) AS snapshot_rank
            FROM hourly_snapshots
        )
        WHERE snapshot_rank = 1
    """)

    # Save the selected forecasts separately from the demonstration output
    connection.execute("""
        COPY latest_weather
        TO 'data/processed/latest_weather.parquet'
        (FORMAT PARQUET)
    """)

    # Show how many rows we started with and how many we kept
    connection.sql("""
        SELECT
            (SELECT COUNT(*) FROM hourly_snapshots) AS downloaded_rows,
            (SELECT COUNT(*) FROM latest_weather) AS latest_rows
    """).show()

    print("Saved latest forecasts to data/processed/latest_weather.parquet")

 # Show which downloads supplied the selected forecasts
    connection.sql("""
        SELECT
            retrieved_at,
            source_file,
            COUNT(*) AS selected_hours
        FROM latest_weather
        GROUP BY retrieved_at, source_file
        ORDER BY retrieved_at DESC
    """).show()

connection.close()  # Close the database connection

print("Saved prepared weather to data/processed/hourly_weather.parquet")
