import json #Help python read the saved weather repsonse
from pathlib import Path #z help python find files

raw_file =Path("data/raw/london_sample.json") #locate our saved sample 
data =json.loads(raw_file.read_text()) #read the file and mkae its contents usable 

hourly =data["hourly"]  #get the hourly weather data 

for name,values in hourly.items():  #Go through each weather field and its list
    print(name, len(values)) # show its name and how many values it contains




