import streamlit as st
import folium
from streamlit_folium import st_folium

import pandas as pd
import numpy as np
import helperfnctions as hf

# url = "https://raw.githubusercontent.com/uhoney/fysiikka_loppuprojekti/refs/heads/main/acc_gps/Location.csv"
url = "./acc_gps/Location.csv"
df = pd.read_csv(url)

# Lisää dataframeen kuljettu matka
df["Travel distance"] = hf.addTravelDistanceToDataFrame(df)

# Title
st.title("Kävely testi")

# Print values
st.write(f'Kokonaismatka: {df["Travel distance"].max():.2f} km')
st.write(f'Keskinopeus: {df["Velocity (m/s)"].max():.2f} m/s')

# draw line plot
st.line_chart(df, x="Time (s)", y="Travel distance", y_label="Distance", x_label="Time")

# Create a map where the center is at start_lat start_long and zoom level is defined
start_lat = df["Latitude (°)"].mean()
start_long = df["Longitude (°)"].mean()
map = folium.Map(location=[start_lat, start_long], zoom_start=15)

# Draw the map
folium.PolyLine(
    df[["Latitude (°)", "Longitude (°)"]], color="blue", weight=3.5, opacity=1
).add_to(map)


# Define map dimensions and show the map
st_map = st_folium(map, width=900, height=650)
