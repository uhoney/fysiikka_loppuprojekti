from math import radians, cos, sin, asin, sqrt
import numpy as np


def haversine(lon1, lat1, lon2, lat2):  # Kahden pisteen koordinaatit
    """
    Calculate the great circle distance in kilometers between two points  on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine kaava
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Maapallon säde
    return c * r  # Palauttaa koordinaattien välisen etäisyyden maapallon pintaa pitkin.


def addTravelDistanceToDataFrame(df):

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
