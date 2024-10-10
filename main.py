import folium.map
import streamlit as st
import folium
from streamlit_folium import st_folium

import pandas as pd
import numpy as np
import apurifunktiot as af

url = "https://raw.githubusercontent.com/uhoney/fysiikka_loppuprojekti/refs/heads/main/linear_acc_gps/Location.csv"
url2 = "https://raw.githubusercontent.com/uhoney/fysiikka_loppuprojekti/refs/heads/main/linear_acc_gps/Linear Acceleration.csv"

# url = "./linear_acc_gps/Location.csv"
# url2 = "./linear_acc_gps/Linear Acceleration.csv"

lokaatio = pd.read_csv(url)
kiihtyvyys = pd.read_csv(url2)

# Lisää dataframeen kuljettu matka,
lokaatio["Travel distance"] = af.lisaaEtaisyydetDataFrameen(lokaatio)

# Askelmäärät, askelpituudet, keskinopeus, kuljettu matka
kuljettuMatka = lokaatio["Travel distance"].max()
keskinopeus = lokaatio["Velocity (m/s)"].mean()
alipaastoKomponentti = af.alipaastoPlottaus(kiihtyvyys, "y", 0.5)
askeleetSuodatettu = af.laskeAskeleet(alipaastoKomponentti)
askelpituusSuodatettu = kuljettuMatka / askeleetSuodatettu
askeleetFourier = af.fourierAskeleet(kiihtyvyys, "y")
askelpituusFourier = kuljettuMatka / askeleetFourier

# Printtailut
st.title("Fysiikan loppuprojekti")
st.write(f"Kuljettu matka: {kuljettuMatka:.2f} km")
st.write(f"Keskinopeus: {keskinopeus:.2f} ms  ({keskinopeus*3.6:.2f} km/h)")
st.write(f"Askeleet (suodatettu): {askeleetSuodatettu}")
st.write(f"Askeleet (fourier): {askeleetFourier}")
st.write(f"Askelpituus (suodatettu): {askelpituusSuodatettu*1000:.2f} m")
st.write(f"Askelpituus (fourier): {askelpituusFourier*1000:.2f} m")

# Kartta piirto
start_lat = lokaatio["Latitude (°)"].mean()
start_lon = lokaatio["Longitude (°)"].mean()
map = folium.Map(location=[start_lat, start_lon], zoom_start=15)
folium.PolyLine(lokaatio[["Latitude (°)", "Longitude (°)"]], color="blue", weight=3, opacity=1).add_to(map)
st.write(f"### Reitti kartalla")
st_map = st_folium(map, width=800, height=600)

# Tehospektri piirto
tehospektri = af.tehospektri(kiihtyvyys, "y")
tehospektri = tehospektri[tehospektri["freq"] <= 10]
st.write(f"### Tehospektri")
st.line_chart(tehospektri, x="freq", y="psd", y_label="Teho", x_label="Taajuus [Hz]")

# Suodatettu kiihtyvyyskomponentti piirto
suodatettuKomponenttiY = pd.DataFrame({"aika": kiihtyvyys["Time (s)"], "suodatettu": alipaastoKomponentti})
suodatettuKomponenttiY = suodatettuKomponenttiY[suodatettuKomponenttiY["aika"] <= 15]
st.write(f"### Suodatettu kiihtyvyyskomponentti Y")
st.line_chart(
    suodatettuKomponenttiY, x="aika", y="suodatettu", x_label="Aika (s)", y_label="Lineaarinen kiihtyvyys y (m/s^2)"
)
