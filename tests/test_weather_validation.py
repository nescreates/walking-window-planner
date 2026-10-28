import json
import sys
import tempfile
import unittest
from pathlib import Path

# Help this test find the code inside our project's src folder
project_folder = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_folder / "src"))

from inspect_weather import validate_weather


class TestWeatherValidation(unittest.TestCase):

    def check_weather(self, rain_probability):
        # Make a small example forecast for our checks
        data = {
            "hourly": {
                "time": ["2026-10-20T20:00"],
                "temperature_2m": [11.8],
                "precipitation_probability": [rain_probability],
            }
        }

        # Use a temporary folder so our real weather files stay untouched
        with tempfile.TemporaryDirectory() as folder:
            sample_file = Path(folder) / "test_weather.json"
            sample_file.write_text(json.dumps(data))

            # Run the same validation function used by preparation
            validate_weather(sample_file)

    def test_valid_weather_passes(self):
        # A 24% chance of rain should be accepted without an error
        self.check_weather(24)

    def test_impossible_rain_is_rejected(self):
        # This test passes only if validation rejects 150%
        with self.assertRaises(ValueError):
            self.check_weather(150)


if __name__ == "__main__":
    unittest.main()
    