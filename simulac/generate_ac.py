import numpy as np
import scipy as sp
import scipy.signal
import sys
import argparse

from pint import UnitRegistry
Q_ = UnitRegistry().Quantity
def toUnits(units):
    return lambda s: Q_(s).to(units)

LIGHT_SPEED = Q_(3e8,'m/s')
parser = argparse.ArgumentParser(description='Sample the autocorrelation of a gaussian beam')
parser.add_argument('--pulse_width', type=toUnits('fs'), default=Q_(40, 'fs'))
parser.add_argument('--wavelength', type=toUnits('nm'), default=Q_(830,'nm'))
parser.add_argument('--sampling', type=float, default=1, help='Factor of the Nyquist sampling frequency to sample the autocorrelation at')
parser.add_argument('--window', type=toUnits('fs'), help='Width of the window sampled')
parser.add_argument('--chirp', type=float, default=0.)
parser.add_argument('output', type=argparse.FileType('wb'))
cfg = parser.parse_args()
if cfg.window is None:
    cfg.window = 10*cfg.pulse_width

angular_frequency = 2*sp.pi*LIGHT_SPEED/cfg.wavelength
sample_frequency = 2.2*angular_frequency/np.pi * cfg.sampling
samples = int((sample_frequency * cfg.window).to('dimensionless'))

def gaussian(t, width=1., chirp=0.):
    return sp.exp(-((0.5+0.5j*chirp)*(t/width)**2))

def autocorrelation_i2(t, envelope, angular_frequency):
    envelopec = sp.conj(envelope)
    envelope2 = envelope*envelope
    envelope_mod2 = envelope*envelopec
    trange = t[-1]-t[0]
    tau = sp.linspace(-trange, trange, 2*len(envelope)-1)
    phase = sp.exp(-1j*angular_frequency*tau)
    interf  = 2*sp.sum(envelope_mod2**2)
    interf += 4*scipy.signal.fftconvolve(envelope2*envelopec,envelope)*phase
    interf += 2*scipy.signal.fftconvolve(envelope2, envelope2)*phase**2
    interf += 4*scipy.signal.fftconvolve(envelope_mod2, envelope_mod2) 
    interf += 4*scipy.signal.fftconvolve(envelope,
                                         envelopec*envelope_mod2)*phase
    interf = np.real(interf)
    return (tau, interf)

t = sp.linspace(-cfg.window/2, cfg.window/2, samples)
pulse = gaussian(t, cfg.pulse_width, cfg.chirp)
(tau, interf) = autocorrelation_i2(t, pulse, angular_frequency)
interf /= np.max(interf)

# Write file
for k in vars(cfg):
    cfg.output.write("# {} = {}\n".format(k, vars(cfg)[k]).encode('ascii'))
cfg.output.write('# tau [fs]\t interf'.encode('ascii'))
np.savetxt(cfg.output, np.vstack((tau, interf)).T)
