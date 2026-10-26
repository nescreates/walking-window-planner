import json #Help python read the saved weather repsonse
from pathlib import Path #z help python find files

raw_file =Path("data/raw/london_sample.json") #locate our saved sample 
data =json.loads(raw_file.read_text()) #read the file and mkae its contents usable 

hourly =data["hourly"]  #get the hourly weather data 



for name,values in hourly.items():  #Go through each weather field and its list
    print(name, len(values)) # show its name and how many values it contains

# Count how many forecast times we have
expected_count = len(hourly["time"])

# Check the two weather fields our app uses
for field in ["temperature_2m", "precipitation_probability"]:
    values = hourly[field]  # Get this field's list of weather values

    if len(values) != expected_count:  # Check whether the counts differ
        raise ValueError(f"{field}: each forecast time needs a matching value.")

print("PASS: every forecast time has a temperature and rain probability.") 

# Check the three lists our app needs
for field in ["time", "temperature_2m", "precipitation_probability"]:
    values = hourly[field]  # Get this field's list

    if None in values:  # Look for an entry with no value
        raise ValueError(f"{field}: a value is missing.")

print("PASS: no missing times, temperatures or rain probabilities.")

 # Check each rain probability is between 0 and 100
for probability in hourly["precipitation_probability"]:
    if not 0 <= probability <= 100:
        raise ValueError("Rain probability must be between 0 and 100.")

print("PASS: all rain probabilities are between 0 and 100.")

# Check that the same forecast time does not appear twice
times = hourly["time"]

if len(times) != len(set(times)):
    raise ValueError("A forecast time appears more than once.")

print("PASS: no repeated forecast times.")

