import streamlit as st
import folium
from streamlit_folium import st_folium

import pandas as pd
import numpy as np
import apurifunktiot as af

# url = "https://raw.githubusercontent.com/uhoney/fysiikka_loppuprojekti/refs/heads/main/acc_gps/Location.csv"
url = "./acc_gps/Location.csv"
url2 = "./acc_gps/Accelerometer.csv"

lokaatio = pd.read_csv(url)
kiihtyvyys = pd.read_csv(url2)

# Lisää dataframeen kuljettu matka
lokaatio["Travel distance"] = af.lisaaEtaisyydetDataFrameen(lokaatio)

kuljettuMatka = lokaatio["Travel distance"].max()
keskinopeus = lokaatio["Velocity (m/s)"].mean()
st.write(f"Kuljettu matka: {kuljettuMatka:.2f} km")
st.write(f"Keskinopeus: {keskinopeus:.2f} ms  ({keskinopeus*3.6:.2f} km/h)")

# Askelmäärä ( filtered )
alipaastoKomponentti = af.alipaastoPlottaus(kiihtyvyys, "z", 0.5)
askeleetSuodatettu = af.laskeAskeleet(alipaastoKomponentti)
askelpituusSuodatettu = kuljettuMatka / askeleetSuodatettu
st.write(f"Askeleet (suodatettu): {askeleetSuodatettu}")
st.write(f"Askelpituus (suodatettu): {askelpituusSuodatettu*1000:.2f} m")

# Askelmäärä ( fourier )
askeleetFourier = af.fourierAskeleet(kiihtyvyys)
askelpituusFourier = kuljettuMatka / askeleetFourier
st.write(f"Askeleet (fourier): {askeleetFourier}")
st.write(f"Askelpituus (fourier): {askelpituusFourier*1000:.2f}")

tehospektri = af.tehospektri(kiihtyvyys)

st.line_chart(tehospektri, x="freq", y="psd", y_label="Teho", x_label="Taajuus [Hz]")
