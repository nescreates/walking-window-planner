import duckdb

connection = duckdb.connect() 
chosen_time = input("Enter a date and hour (YYYY-MM-DD HH:00:00): ")  # Ask which forecast to show
query = """
WITH hourly_weather AS (
    -- First, arrange the saved weather into rows
    SELECT
        CAST(unnest(hourly.time) AS TIMESTAMP) AS forecast_time,
        unnest(hourly.temperature_2m) AS temperature_c,
        unnest(hourly.precipitation_probability) AS rain_probability_pct
    FROM read_json_auto('data/raw/london_sample.json')
)
SELECT *
FROM hourly_weather
WHERE forecast_time = CAST(? AS TIMESTAMP) -- Use the time entered by the user
ORDER BY forecast_time; -- Show every forecast hour in time order
"""
result = connection.sql(query, params=[chosen_time])  # Look up the chosen time
rows = result.fetchall()  # Bring the matching rows into Python

if not rows:  # If no matching rows were found
    print("No forecast found for that time in the saved data.")
else:  # Otherwise, show the forecast
    result.show()

connection.close() # close the connection to the database when finished 
 