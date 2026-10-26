# Walking window planner 

## What i built and who for 

For working prfoessisonals working desk based or jobs 

who want to incorprate for cardio or steps in their working day

Assit them in choosing their perferrred weather prefernce to walk according the their work schedule 

## First Version Scope 
The first version lets a user choose a date and hour to check the forecast temperature and chance of rain before a planned walk.

Currently, the script uses a saved London forecast sample covering 20 October 2026. It accepts an exact hour and displays the matching forecast, or a clear message if no matching forecast is available.

It does not currently suggest walking times, calculate routes or track steps.

## What i would do next 
Features that could be added later ; recommednds best routes to take based on their current location and step goals they want to acheive everyday or per week.

## How it works

1. Collect the weather data
   A Python script requests an hourly forecast from Open-Meteo for London, including temperature and chance of rain.

2. Save the original response
   The script saves the response in data/raw/london_sample.json without changing its contents. This lets us work from the same sample without requesting the API again.

3. Inspect the saved data
   A separate script checks how many entries each hourly list contains. In our sample, the times, temperatures and rain probabilities each contain 24 entries.

5. Look up the chosen forecast
   The user enters a date and hour. Python passes this choice to a SQL query, which finds the matching forecast.

6. Handle unavailable forecasts
   If no matching row exists in the saved data, the script displays a message instead of an empty table.

The current script identifies hours matching these example weather preferences. Availability and walking duration will be added next. Wind is outside the first version's scope.
## Scope decision


I simplified the first version to answer one question: “What weather should I expect at my chosen walking time?”

Earlier experiments filtered weather conditions and availability to suggest walking times. The current version focuses on checking a time the user has already chosen.

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

AI also provided example SQL and Python code for the forecast lookup and missing-result handling. I ran manual checks using a time present in the sample and a date outside it.

## Checks performed

I manually checked these situations:

- A time available in the sample returns its forecast.
- A date outside the sample displays a “No forecast found” message.
- An entry such as `hello` displays guidance on the expected date format.
- A time such as `20:30:00` asks the user to choose an exact hour.
- Added checks for matching list lengths, missing values, rain probabilities between 0 and 100, and repeated forecast times.
- Manually tested the rain probability check by temporarily setting one value to 150 in memory. The script rejected it.
- Removed the temporary change and confirmed all four checks passed on the saved sample.
These are manual checks; automated tests are not implemented yet.

