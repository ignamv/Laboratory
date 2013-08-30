import argparse
import numpy as np
from matplotlib import pyplot as plt
from pint import UnitRegistry
from generate_ac import gaussian, autocorrelation_i2
from mosaic import mosaic
from chirp import mosaicPeak
from toUnits import toUnits
import tiza
from . import Q_

LIGHT_SPEED = Q_(3e8,'m/s')

parser = argparse.ArgumentParser(description='MOSAIC-analyze gaussian pulses of varying chirp, test variation of MOSAIC peak with chirp')
parser.add_argument('--chirp_min', type=float, default=0)
parser.add_argument('--chirp_max', type=float, default=2)
parser.add_argument('--steps', type=int, default=10)
parser.add_argument('--pulse_width', type=toUnits('fs'),
                    default=tiza.pulse_width)
parser.add_argument('--wavelength', type=toUnits('nm'),
                    default=tiza.wavelength)
parser.add_argument('--window', type=toUnits('fs'), help='Width of the window sampled')
parser.add_argument('--sampling', type=float, default=1, help='Factor of the Nyquist sampling frequency to sample the autocorrelation at')
cfg = parser.parse_args()
if cfg.window is None:
    cfg.window = 10*cfg.pulse_width

angular_frequency = 2*np.pi*LIGHT_SPEED/cfg.wavelength
sample_frequency = 2.2*angular_frequency/np.pi * cfg.sampling
print(LIGHT_SPEED)
print(cfg.wavelength)
print(angular_frequency)
print(sample_frequency)
print(cfg.window)
samples = int((sample_frequency * cfg.window).to('dimensionless'))

t = np.linspace(-cfg.window/2, cfg.window/2, samples)
def simulateMosaicPeak(chirp):
    pulse = gaussian(t, cfg.pulse_width, chirp)
    (tau, interf) = autocorrelation_i2(t, pulse, angular_frequency)
    return mosaicPeak(mosaic(interf))

chirps = np.linspace(cfg.chirp_min, cfg.chirp_max, cfg.steps)
peaks = np.vectorize(simulateMosaicPeak)(chirps)

plt.figure()
plt.plot(chirps, peaks, 'rx')
plt.xlabel('Chirp')
plt.ylabel('MOSAIC peak')
plt.show()
print(chirps)
print(peaks)
