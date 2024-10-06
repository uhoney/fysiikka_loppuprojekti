import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):  # Kahden pisteen koordinaatit
    """
    Calculate distance in kilometers between two points on earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth
    return c * r


def addTravelDistanceToDataFrame(df):
    """
    Adds distances to dataframe between poins in kilometers
    """
    lat = df["Latitude (°)"]
    lon = df["Longitude (°)"]

    tmp_distances = np.zeros(
        len(df)
    )  # Alusta väliaikainen array nollaksi, tallennetaan etäisyydet siihen

    # Jos halutaan varmistua, että laskeminen aloitetaan nollasta, voi syöttää .insert() nollaindeksin
    # Tässä on kuitenkin alustettu jo nollaksi, joten aloitetaan suoraan vain laskut indeksistä 1
    # Välillä meni dataframe sekaisin, kun oli eri pituuksia.
    for i in range(1, len(df) - 1):
        tmp_distances[i] = haversine(lon[i], lat[i], lon[i + 1], lat[i + 1])

    return np.cumsum(tmp_distances)


def butter_lowpass(data, cutoff, nyq, order):
    normal_cutoff = cutoff / nyq
    # filter coefficients
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    y = filtfilt(b, a, data)
    return y


def butter_highpass(data, cutoff, nyq, order):
    normal_cutoff = cutoff / nyq
    # filter coefficients
    b, a = butter(order, normal_cutoff, btype="high", analog=False)
    y = filtfilt(b, a, data)
    return y


def filterWithButterLow(tmp, component, cutoff):
    """
    TODO: add description
    """
    # Filter parameters:
    T = tmp["Time (s)"][len(tmp["Time (s)"]) - 1] - tmp["Time (s)"][0]
    n = len(tmp["Time (s)"])  # Datapisteiden määrä
    fs = n / T  # Näytteenottotaajuus (oletus, että jotekuten vakio)
    nyq = fs / 2  # Nyquist-taajuus
    order = 3  # Kertaluku
    cutoff = 1 / (cutoff)  # Cutoff-taajuus

    # Valitun komponentin suodatus butter_lowpassilla
    filtered_low = butter_lowpass(tmp[f"Acceleration {component} (m/s^2)"], cutoff, nyq, order)

    return filtered_low


def getStepsFromFilteredData(filteredComponent):
    """
    TODO: add description
    """
    # Laske x-akselin ylitykset ajanjaksolla. return askelmäärä
    crossing = 0
    for i in range(len(filteredComponent) - 1):
        if filteredComponent[i] / filteredComponent[i + 1] < 0:
            crossing += 1

    return int(np.floor(crossing / 2))
