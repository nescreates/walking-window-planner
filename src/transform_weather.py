import duckdb

connection = duckdb.connect() 
query = """
SELECT 
      unnest(hourly.time) AS forecast_time, -- put each time on its own row 
      unnest (hourly.temperature_2m) AS temperature_c -- put its temperature beside it 
FROM read_json_auto('data/raw/london_sample.json');
"""

connection.sql(query).show() #Run our SQL and disply the results in terminal 

connection.close() # close the connection to the database when finished 
 