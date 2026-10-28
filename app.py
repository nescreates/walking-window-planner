from pathlib import Path
import duckdb
import streamlit as st

# Set the browser tab title and page heading
st.set_page_config(page_title="Walking Window Planner")
st.title("Walking Window Planner")
st.write("Check London's forecast before your planned walk.")
st.info("This app uses saved forecasts. It does not fetch current weather.")

# Let the user choose which saved data to explore
dataset = st.selectbox(
    "Choose weather data",
    ["Demonstration sample", "Downloaded forecasts"],
)

# Find our data folder starting from this app's location
project_folder = Path(__file__).resolve().parent
filename = (
    "hourly_weather.parquet"
    if dataset == "Demonstration sample"
    else "latest_weather.parquet"
)
prepared_file = project_folder / "data" / "processed" / filename

# Explain what to do if preparation has not been run
if not prepared_file.is_file():
    st.error("Prepared data is missing. Run python src/prepare_weather.py first.")
    st.stop()

# Open DuckDB and close it even if something goes wrong
connection = duckdb.connect()

try:
    # Read the available times so we only offer times we have data for
    time_rows = connection.execute("""
        SELECT DISTINCT forecast_time
        FROM read_parquet(?)
        ORDER BY forecast_time
    """, [str(prepared_file)]).fetchall()

    if not time_rows:
        st.warning("There are no forecast times in this dataset.")
        st.stop()

    # Take each time out of its database row
    available_times = [row[0] for row in time_rows]

    chosen_time = st.selectbox(
        "Choose your walking date and hour — London local time",
        available_times,
    )

    # Find the weather for the selected time
    forecast = connection.execute("""
        SELECT temperature_c, rain_probability_pct
        FROM read_parquet(?)
        WHERE forecast_time = ?
    """, [str(prepared_file), chosen_time]).fetchone()

    if forecast is None:
        st.warning("No forecast was found for that time.")
        st.stop()

    # Display the two values with readable labels and units
    st.metric("Temperature", f"{forecast[0]:.1f} °C")
    st.metric("Chance of rain", f"{forecast[1]:.0f}%")

    if dataset == "Downloaded forecasts":
        # Show when we collected the selected forecast
        source = connection.execute("""
            SELECT retrieved_at, source_file
            FROM read_parquet(?)
            WHERE forecast_time = ?
        """, [str(prepared_file), chosen_time]).fetchone()

        st.caption(f"Downloaded at: {source[0]} (UTC)")
        with st.expander("View original source filename"):
            st.text(source[1])
    else:
        st.caption("Demonstration forecast for 20 October 2026.")

    st.caption("Weather data: Open-Meteo · CC BY 4.0")

finally:
    connection.close()