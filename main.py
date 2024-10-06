import streamlit as st
import folium
from streamlit_folium import st_folium

import pandas as pd
import numpy as np
import helperfunctions as hf

# url = "https://raw.githubusercontent.com/uhoney/fysiikka_loppuprojekti/refs/heads/main/acc_gps/Location.csv"
url = "./acc_gps/Location.csv"
url2 = "./acc_gps/Accelerometer.csv"

location = pd.read_csv(url)
acceleration = pd.read_csv(url2)

# Lisää dataframeen kuljettu matka
location["Travel distance"] = hf.addTravelDistanceToDataFrame(location)

# Kuljettu matka
totalDistanceTravelled = location["Travel distance"].max()

# Keskinopeus
averageSpeed = location["Velocity (m/s)"].max()

# Suodata kiihtyvyskomponentti scipyn butter lowpassilla
filteredAccelerationData = hf.filterWithButterLow(acceleration, "z", 0.5)
stepsFromFilteredData = hf.getStepsFromFilteredData(filteredAccelerationData)

# Askelpituus suodatetusta datasta
strideLengthFromFilteredData = (totalDistanceTravelled / stepsFromFilteredData) * 1000


# TODO: Fourier analyysit

# chart_data = pd.DataFrame(np.transpose(np.array([freq[L], psd[L].real])), columns=["freq", "psd"])
# st.line_chart(chart_data, x="freq", y="psd", y_label="Teho", x_label="Taajuus [Hz]")

# Title
st.title("Fysiikka loppuprojekti")

st.write(f"""#### Kuljettu matka (location): {totalDistanceTravelled:.2f} km""")
st.write(f"""#### Keskinopeus (location): {averageSpeed:.2f} m/s""")
st.write(f"""#### Askelpituus (accelerometer): {strideLengthFromFilteredData:.2f} m""")
st.write(f"""#### Askeleet (accelerometer, filtered): {stepsFromFilteredData}""")
st.write(f"""#### Askeleet (accelerometer, fourier): {0}""")


# draw line plot
st.line_chart(location, x="Time (s)", y="Travel distance", y_label="Distance", x_label="Time")

# Create a map where the center is at start_lat start_long and zoom level is defined
start_lat = location["Latitude (°)"].mean()
start_long = location["Longitude (°)"].mean()
map = folium.Map(location=[start_lat, start_long], zoom_start=15)

# Draw the map
folium.PolyLine(
    location[["Latitude (°)", "Longitude (°)"]], color="blue", weight=3.5, opacity=1
).add_to(map)

# Define map dimensions and show the map
st_map = st_folium(map, width=900, height=650)
