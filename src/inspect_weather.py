import json  # Help Python read the saved weather response
from pathlib import Path  # Help Python find files


def validate_weather(raw_file):
    raw_file = Path(raw_file)  # Find the file we were asked to check
    data = json.loads(raw_file.read_text())  # Read the saved weather
    hourly = data["hourly"]  # Get the hourly weather values

    # Show how many entries each weather list contains
    for name, values in hourly.items():
        print(name, len(values))

    # Count how many forecast times we have
    expected_count = len(hourly["time"])

    # Check each time has a matching temperature and rain probability
    for field in ["temperature_2m", "precipitation_probability"]:
        values = hourly[field]  # Get this field's list

        if len(values) != expected_count:
            raise ValueError(
                f"{field}: each forecast time needs a matching value."
            )

    print("PASS: every forecast time has a temperature and rain probability.")

    # Check that none of the entries we need are missing
    for field in ["time", "temperature_2m", "precipitation_probability"]:
        values = hourly[field]  # Get this field's list

        if None in values:  # None means an entry has no value
            raise ValueError(f"{field}: a value is missing.")

    print("PASS: no missing times, temperatures or rain probabilities.")

    # Check every rain probability is at least 0 and at most 100
    for probability in hourly["precipitation_probability"]:
        if not 0 <= probability <= 100:
            raise ValueError("Rain probability must be between 0 and 100.")

    print("PASS: all rain probabilities are between 0 and 100.")

    # Check that the same forecast time does not appear twice
    times = hourly["time"]

    # A set keeps only unique values, so repeats would reduce the count
    if len(times) != len(set(times)):
        raise ValueError("A forecast time appears more than once.")

    print("PASS: no repeated forecast times.")


# Run this part only when we run this file directly
if __name__ == "__main__":
    validate_weather("data/raw/london_sample.json")