import argparse
import numpy as np
from toUnits import toUnits

parser = argparse.ArgumentParser(description='MOSAIC-analyze gaussian pulses of varying chirp, test variation of MOSAIC peak with chirp')
parser.add_argument('--chirp_min', type=float, default=0)
parser.add_argument('--chirp_max', type=float, default=2)
parser.add_argument('--steps', type=int, default=10)
parser.add_argument('--pulse_width', type=toUnits('fs'), default=Q_(40, 'fs'))
cfg = parser.parse_args()

chirps = np.linspace(cfg.chirp_min, cfg.chirp_max, cfg.steps)
t = sp.linspace(-cfg.window/2, cfg.window/2, samples)
for chirp in chirps:
    pulse = gaussian(t, cfg.pulse_width, chirp)
    (tau, interf) = autocorrelation_i2(t, pulse, angular_frequency)
    interf /= np.max(interf)
