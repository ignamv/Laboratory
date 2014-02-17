import argparse
import numpy as np
import numpy
import scipy.signal
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser('Plot peaks')
parser.add_argument('input', type=argparse.FileType('r'))

cfg = parser.parse_args()

tau, interf = np.loadtxt(cfg.input, unpack=True)

peaks = scipy.signal.argrelmax(interf)

plt.figure()
plt.plot(tau, interf, label='AC')
plt.plot(tau[peaks], interf[peaks], 'rx', label='Peaks')
plt.show()

