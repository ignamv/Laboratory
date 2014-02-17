import argparse
import numpy as np
import numpy
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser('Plot spectrum')
parser.add_argument('input', type=argparse.FileType('r'))

cfg = parser.parse_args()

tau, interf = np.loadtxt(cfg.input, unpack=True)

spectrum = numpy.fft.fftshift(numpy.fft.fft(interf))
freq = numpy.fft.fftshift(numpy.fft.fftfreq(len(interf), tau[1]-tau[0]))

plt.figure()
plt.plot(freq, np.abs(spectrum))
plt.show()
