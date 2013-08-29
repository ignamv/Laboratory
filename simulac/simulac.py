import scipy as sp
import numpy as np
import scipy.signal
import scipy.interpolate
import numpy.fft as fft
import os
from matplotlib import pyplot as plt
from lantz import Q_


if 0:
    spectrum = fft.fftshift(fft.fft(interf))
    plt.figure()
    plt.plot(fft.fftshift(fft.fftfreq(len(spectrum), t[1]-t[0])),
             np.log(np.abs(spectrum)),label='Original')
    plt.plot([sample_frequency.to('1/fs').magnitude], [0], 'o')
    spectrum = fft.fftshift(fft.fft(samples))
    plt.plot(fft.fftshift(fft.fftfreq(len(spectrum),
                                      sample_times[1]-sample_times[0])),
             np.log(np.abs(spectrum)),label='Sampled')
    plt.xlabel('Frequency [{}]'.format(1/tau.units))
    plt.title('Spectrum')

if 0:
    plt.figure()
    plt.plot(t, np.real(pulse*np.exp(1j*angular_frequency*t)))

# ---------- CALCULATE ENVELOPE ---------------------------------------------
peaks = scipy.signal.argrelmax(interf)
xpeaks = tau[peaks]
ypeaks = interf[peaks]

plt.figure()
plt.plot(tau, interf, label="Signal")
plt.plot(xpeaks, ypeaks, 'rx', label="Envelope")
plt.xlabel('$\\tau$ [{}]'.format(tau.units))
plt.legend()
plt.title('Original')

if 0:
    plt.figure()
    plt.plot(sample_times, samples)
    plt.xlabel('$\\tau$ [{}]'.format(tau.units))
    plt.title('Sampled')
    plt.show()
