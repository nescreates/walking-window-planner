import duckdb

connection = duckdb.connect() 
query = """
WITH hourly_weather AS (
    -- First, arrange the saved weather into rows
    SELECT
        unnest(hourly.time) AS forecast_time,
        unnest(hourly.temperature_2m) AS temperature_c,
        unnest(hourly.precipitation_probability) AS rain_probability_pct
    FROM read_json_auto('data/raw/london_sample.json')
)
SELECT *
FROM hourly_weather
WHERE rain_probability_pct <= 25 -- Keep hours within the rain limit
AND temperature_c BETWEEN 12 AND 20 -- Also keep temperatures from 12 to 20 degrees
ORDER BY forecast_time; -- Show the results in time order
"""
connection.sql(query).show() #Run our SQL and disply the results in terminal 

connection.close() # close the connection to the database when finished 
 