import numpy as np
import pandas as pd
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

    return pd.DataFrame(
        np.transpose(np.array([freq[L], psd[L].real])), columns=["freq", "psd"]
    )
