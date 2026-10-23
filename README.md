# Walking window planner 

## What i built and who for 

For working prfoessisonals working desk based or jobs 

who want to incorprate for cardio or steps in their working day

Assit them in choosing their perferrred weather prefernce to walk according the their work schedule 

## First Version Scope 
The user would enter : weather preferences, location,avaiable start/end time and desried walking duration for version 1.

Available time means time the user can actually spend walking; meals and other buffers are already accounted for.

The app would return ;suggest walking windows that fit the user’s availability, duration and weather preferences, with forecast conditions and an explanation. If none fit, explain why.

## What i would do next 
Features that could be added later ; recommednds best routes to take based on their current location and step goals they want to acheive everyday or per week.

## How it works
## How it works

1. Collect the weather data
   A Python script requests an hourly forecast from Open-Meteo for London, including temperature and chance of rain.

2. Save the original response
   The script saves the response in data/raw/london_sample.json without changing its contents. This lets us work from the same sample without requesting the API again.

3. Inspect the saved data
   A separate script checks how many entries each hourly list contains. In our sample, the times, temperatures and rain probabilities each contain 24 entries.

4. Arrange the data into rows
   DuckDB runs SQL that pairs each time with its temperature and rain probability, creating one row per forecast hour.

5. Apply example weather preferences
   SQL keeps hours with a rain probability of 25% or less and a temperature between 12°C and 20°C, including the limits.

The current script identifies hours matching these example weather preferences. Availability and walking duration will be added next. Wind is outside the first version's scope.


## How to run it
python -m pip install -r requirements.txt
python src/fetch_weather.py
python src/inspect_weather.py
python src/transform_weather.py

## Where AI helped

Scope: defining the user, inputs, outputs and first-version boundaries.
Setup: providing Git commands, virtual-environment instructions and .gitignore entries.
Code: providing the Python examples for requesting, saving and inspecting weather data.
Understanding and debugging: explaining the code, reviewing screenshots and correcting misunderstanding