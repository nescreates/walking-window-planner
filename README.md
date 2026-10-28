# Walking Window Planner

## What I built and who for

A command-line forecast lookup for desk-based workers who want to check the weather before a planned walk.

The user enters a date and exact hour to see the forecast temperature and precipitation probability.

The current version demonstrates a Python and SQL pipeline using a saved London forecast for 20 October 2026. It is not a live weather app.

## The data

Source: [Open-Meteo Forecast API](https://open-meteo.com/en/docs).

The included sample contains 24 hourly forecasts for London, with the API configured to use Europe/London time.

The lookup uses:

- Forecast time.
- Temperature in degrees Celsius.
- Precipitation probability as a percentage.

The original response also contains wind speed, which this version does not use.

The original JSON is stored unchanged in `data/raw/london_sample.json`. Keeping a sample allows reviewers to reproduce the example without calling the API.

Weather data is provided by [Open-Meteo](https://open-meteo.com/) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This project reshapes selected fields into a table; it does not create the forecasts.

## How it works

1. **Extract:** `src/fetch_weather.py` requests an hourly London forecast and saves the original JSON response.

2. **Validate:** `src/inspect_weather.py` provides a reusable function that checks matching list lengths, missing values, precipitation probabilities between 0 and 100, and repeated forecast times.

3. **Transform and save:** `src/prepare_weather.py` calls validation before using DuckDB SQL to turn the separate hourly lists into rows. It converts time strings into timestamps, gives the columns readable names and saves `data/processed/hourly_weather.parquet`.

4. **Look up:** `src/lookup_weather.py` reads the prepared table. It passes the user's chosen time to a parameterised SQL query and displays the matching forecast.

If validation fails, preparation stops. The lookup also handles invalid date entries, times outside exact hours, unavailable forecasts and a missing prepared file.

Preparation and lookup are separate so multiple lookups can reuse the prepared table. Running preparation again replaces the output rather than appending rows.

The generated `data/processed/` folder is excluded from Git because it can be recreated from the original sample.

### Scope decision

I initially explored recommending walking times based on weather preferences and availability. I simplified the first version to answer:

“What weather should I expect at my chosen walking time?”

This keeps the first version focused on preparing reliable data and retrieving the chosen forecast.

## How to run it

These instructions are for macOS/Linux. Python 3.13.7 was used during development.

Run commands from the project folder.

Create and activate a virtual environment:

When prompted, choose `1` for the demonstration sample, then enter:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Prepare the included sample:

```bash
python src/prepare_weather.py
```
Expected output includes validation messages, 24 demonstration rows,
and a summary of the downloaded forecasts processed.

Start the lookup:

```bash
python src/lookup_weather.py
```
When prompted, choose `1` for the demonstration sample, then enter:

```text
2026-10-20 20:00:00
```

Expected result: 11.8°C and 24% precipitation probability.

Once dependencies are installed, this example runs without an API call. The included forecast is demonstration data, not current weather.

### Fetching new data

```bash
python src/fetch_weather.py
```
Preparation also processes the timestamped downloads in `data/raw/live/`.
For each location and forecast hour, SQL selects the most recently
downloaded record and saves it to `data/processed/latest_weather.parquet`.
The original JSON downloads remain unchanged.

When running the lookup, choose:
- `1` for the original demonstration sample.
- `2` for the prepared downloaded forecasts.

Option 2 uses saved downloads; it does not request fresh weather automatically.

## Checks performed

The scripts automatically check data and user inputs when run. I manually exercised the following scenarios:

- An available forecast time returns the expected values.
- A date outside the sample produces a “No forecast found” message.
- An entry such as `hello` produces date-format guidance.
- A time such as `20:30:00` asks for an exact hour.
- All four data-quality checks pass on the included sample.
- Temporarily setting a rain probability to 150 in memory triggers rejection. Removing the temporary change restores the passing result.
- Temporarily renaming the Parquet file produces preparation instructions. The file was restored afterwards.
- Repeating preparation still produces 24 rows, and the lookup returns the same example forecast.
- Cloned the GitHub repository into a separate folder, created a new virtual environment, installed the requirements and successfully ran preparation and the example lookup without fetching new weather data. This was tested on the same Mac.
- Processed two downloads covering the same 24 forecast hours: 48 input
  rows became 24 selected rows.
- Checked the selected rows' source filename and retrieval time:
  all 24 came from the newer download.
- Confirmed both lookup options returned forecasts from their respective datasets.
- Confirmed the downloaded-forecast lookup displays the selected record's
  retrieval time and original source filename alongside the weather result.

### Automated tests

Run from the project folder:

```bash
python -m unittest discover -s tests -v
```

Two automated tests check that valid weather data passes validation
and a rain probability of 150% raises a ValueError.
They use temporary files and leave the original weather data unchanged.
Other validation rules and forecast selection are not yet covered by automated tests.

## Limitations

- London is fixed; users cannot select another location.
- The included sample covers one day and is not current weather.
- Only exact hours are supported.
- Forecast timestamps are stored without timezone information; broader date and timezone support needs further work.
- Data checks do not verify forecast accuracy.
- There is no web interface, cloud deployment, route planning or step tracking.

## What I would do next

- Add automated tests for valid and invalid data.
- Check required fields, numeric types and empty datasets.
- Add location selection and clearer timezone handling.
- Build a small web interface using the same prepared dataset.
- Explore weather-based walking recommendations after completing the forecast lookup.

## Where AI helped

AI helped define the scope, explain Python and SQL, suggest Git and environment commands, and troubleshoot errors from terminal output and screenshots.

AI supplied example code for API requests, saving JSON, validation, SQL transformation, Parquet output and forecast lookup.

I used these examples, ran the scripts locally and manually checked the scenarios documented above. I chose to simplify the scope and exclude wind, routes and step tracking from the first version.

AI assistance was substantial. Understanding and explaining the implementation independently remains part of my preparation.