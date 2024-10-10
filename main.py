import folium.map
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from scipy.signal import butter, filtfilt


def haversine(lon1, lat1, lon2, lat2):  # Kahden pisteen koordinaatit
    """
    Laske etäisyys kilometreissä kahden pisteen välillä maapallon pinnalla
    """

    # desimaalit radiaaneiksi
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Maapallon säde
    return c * r


def lisaaEtaisyydetDataFrameen(df):
    """
    Lisää etäisyydet dataframeen
    """
    lat = df["Latitude (°)"]
    lon = df["Longitude (°)"]

    # Alusta väliaikainen array nollaksi, tallennetaan etäisyydet siihen
    tmp_etaisyydet = np.zeros(len(df))

    # Jos halutaan varmistua, että laskeminen aloitetaan nollasta, voi syöttää .insert() nollaindeksin
    # Tässä on kuitenkin alustettu jo nollaksi, joten aloitetaan suoraan vain laskut indeksistä 1
    # Välillä meni dataframe sekaisin, kun oli eri pituuksia.
    for i in range(1, len(df) - 1):
        tmp_etaisyydet[i] = haversine(lon[i], lat[i], lon[i + 1], lat[i + 1])

    return np.cumsum(tmp_etaisyydet)


def alipaastoPlottaus(dataframe, component, cutoff):
    T = dataframe["Time (s)"][len(dataframe["Time (s)"]) - 1] - dataframe["Time (s)"][0]
    n = len(dataframe["Time (s)"])  # Number of data points
    fs = n / T  # Sampling frequency (assuming somewhat constant)
    nyq = fs / 2  # Nyquist frequency
    order = 3  # Filter order
    cutoff = 1 / cutoff  # Cutoff frequency
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)

    filtered_low = filtfilt(b, a, dataframe[f"Linear Acceleration {component} (m/s^2)"])

    return filtered_low


def laskeAskeleet(filteredComponent):
    # Laske x-akselin ylitykset ajanjaksolla. return askelmäärä
    crossing = 0
    for i in range(len(filteredComponent) - 1):
        if filteredComponent[i] / filteredComponent[i + 1] < 0:
            crossing += 1

    return int(np.floor(crossing / 2))


def fourierAskeleet(dataframe, component):
    f = dataframe[f"Linear Acceleration {component} (m/s^2)"]
    t = dataframe["Time (s)"]  # Aika
    N = len(dataframe)  # Havaintojen määrä
    dt = np.mean(np.diff(t))  # Keskimääräinen näytteenottoväli
    fourier = np.fft.fft(f, N)
    psd = fourier * np.conj(fourier) / N  # Tehospektri
    freq = np.fft.fftfreq(N, dt)  # Taajuudet

    L = np.arange(1, int(N / 2))  # Rajataan pois nollataajuus ja negatiiviset taajuudet

    return round(freq[L][psd[L] == np.max(psd[L])][0] * np.max(t))


def tehospektri(dataframe, component):
    f = dataframe[f"Linear Acceleration {component} (m/s^2)"]
    t = dataframe["Time (s)"]  # Aika
    N = len(dataframe)  # Havaintojen määrä
    dt = np.mean(np.diff(t))  # Keskimääräinen näytteenottoväli
    fourier = np.fft.fft(f, N)
    psd = fourier * np.conj(fourier) / N  # Tehospektri
    freq = np.fft.fftfreq(N, dt)
    L = np.arange(1, int(N / 2))

    return pd.DataFrame(np.transpose(np.array([freq[L], psd[L].real])), columns=["freq", "psd"])


url = "https://raw.githubusercontent.com/uhoney/fysiikka_loppuprojekti/refs/heads/main/linear_acc_gps/Location.csv"
url2 = "https://raw.githubusercontent.com/uhoney/fysiikka_loppuprojekti/refs/heads/main/linear_acc_gps/Linear%20Acceleration.csv"

# url = "./linear_acc_gps/Location.csv"
# url2 = "./linear_acc_gps/Linear Acceleration.csv"


lokaatio = pd.read_csv(url)
kiihtyvyys = pd.read_csv(url2)

# Lisää dataframeen kuljettu matka,
lokaatio["Travel distance"] = lisaaEtaisyydetDataFrameen(lokaatio)

# Askelmäärät, askelpituudet, keskinopeus, kuljettu matka
kuljettuMatka = lokaatio["Travel distance"].max()
keskinopeus = lokaatio["Velocity (m/s)"].mean()
alipaastoKomponentti = alipaastoPlottaus(kiihtyvyys, "y", 0.5)
askeleetSuodatettu = laskeAskeleet(alipaastoKomponentti)
askelpituusSuodatettu = kuljettuMatka / askeleetSuodatettu
askeleetFourier = fourierAskeleet(kiihtyvyys, "y")
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
tehospektri = tehospektri(kiihtyvyys, "y")
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
