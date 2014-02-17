import numpy as np
from numpy import fft

t = np.linspace(0,1,100)
y = np.cos(2*np.pi*t)

spec = fft.fftshift(fft.fft(y))
freq = fft.fftshift(fft.fftfreq(len(y), t[1]-t[0]))

from matplotlib import pyplot as plt
plt.plot(freq, spec)
plt.show()
