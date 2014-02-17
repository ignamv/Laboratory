import numpy as np
from lantz import Q_
import os
from matplotlib import pyplot as plt

# Measure a ramp with a multimeter
# The difference between successive samples is proportional to the sample period

# Peak-to-peak voltage
VPP = 100e-3

voltages,times = np.loadtxt(os.sys.argv[1]).transpose()
deltaV = voltages[1:]-voltages[:-1]
deltaT = times[1:]-times[:-1]
deltaT = deltaT[deltaV > 0] * 1e3
deltaV = deltaV[deltaV > 0]

dt = deltaV / VPP * 1e3

plt.figure()
plt.plot(deltaT, dt, 'o')
plt.ylabel('deltaT rampa [ms]')
plt.xlabel('deltaT PC [ms]')
plt.figtext(0.5,0.8,'$\\Delta T = ({:.3f} \\pm {:.3f})$ms'.format(np.mean(dt),np.std(dt)))
plt.savefig(os.path.splitext(os.sys.argv[1])[0]+'.pdf')
plt.show()
