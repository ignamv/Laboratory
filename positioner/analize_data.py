import numpy as np
import os
from matplotlib import pyplot as plt
from os import listdir

"""Analyze the output of test_positioner.py
"""
output_directory = 'C:\\ignacio\\mediciones\\posicionador'

if len(os.sys.argv) == 2:
    filename = os.sys.argv[1]
else:
    filename = output_directory + '\\' + sorted(filename for filename in 
               listdir(output_directory) if filename[:7]=='testrun' and 
               filename[-4:]=='.csv')[-1]
prefix = filename[:filename.rfind('.')] + '_'

positioner, lvdt = np.loadtxt(filename, delimiter=',').transpose()
line = np.polyfit(positioner, lvdt, 1)
print('Linear fit: LVDT = Positioner * {:f} + {:+f}mm'.format(line[0], line[1]))
line_values = np.polyval(line, positioner)
residuals = lvdt - line_values

from matplotlib import pyplot as plt
plt.figure()
plt.plot(positioner, line_values, 'b-', label='Linear fit')
plt.plot(positioner, lvdt, 'rx', label='Measured')
plt.xlabel('Positioner reading [mm]')
plt.ylabel('LVDT reading [mm]')
plt.legend(loc='upper left')
plt.savefig(prefix + 'linearfit.pdf')

plt.figure()
plt.plot(positioner, np.repeat(0,len(line_values)), 'k-')
plt.plot(positioner, residuals, 'gx')
plt.xlabel('Positioner reading [mm]')
plt.ylabel('Residual [mm]')
plt.savefig(prefix + 'residuals.pdf')

relative_error = residuals/lvdt
yrange = 3*np.std(relative_error)
filtered = [x for x in relative_error if abs(x) < yrange]

plt.figure()
plt.plot(positioner, np.repeat(0,len(line_values)), 'k-')
plt.plot(positioner, residuals/lvdt, 'gx')
plt.ylim((-yrange,yrange))
plt.xlabel('Positioner reading [mm]')
plt.ylabel('Relative error')
plt.savefig(prefix + 'relative_error.pdf')

plt.figure()
plt.hist(residuals)
plt.xlabel('Residual [mm]')
plt.ylabel('Count')
plt.savefig(prefix + 'residual_histogram.pdf')

plt.figure()
plt.hist(filtered)
plt.xlabel('Relative error')
plt.ylabel('Count')
plt.savefig(prefix + 'relative_error_histogram.pdf')
