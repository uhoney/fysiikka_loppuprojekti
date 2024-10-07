f = data
N = len(f)  # Havaintojen määrä
fourier = np.fft.fft(f, N)  # Fourier-muunnos
psd = fourier * np.conj(fourier) / N  # Tehospektri
freq = np.fft.fftfreq(N, dt)  # Taajuudet
L = np.arange(1, int(N / 2))  # Rajataan pois nollataajuus ja negatiiviset taajuudet

dt = 0.1  # Oletetaan, että signaali on sämplätty 0.1 s välein
f = df["Acceleration y (m/s^2)"]  # Signaali
N = len(f)  # Pisteiden määrä
fourier = np.fft.fft(f, N)  # Fourier-muunnos
psd = fourier * np.conj(fourier) / N  # Tehospektri
freq = np.fft.fftfreq(N, dt)  # Taajuudet
L = np.arange(1, int(N / 2))
plt.plot(freq[L], psd[L].real)
plt.show()
