from esp300 import ESP300
import numpy as np
from lantz import Q_
from lvdt import LVDT
from os import listdir
from time import sleep

"""Test repeatability of positioner by measuring the spread of successive visits to a location using a LVDT
"""

axis = 1
calibration_file = 'C:\\ignacio\\mediciones\\lvdt\\calibracion lvdt.csv'
oscilloscope_resource = 'GPIB0::14::INSTR'
output_directory = 'C:\\ignacio\\mediciones\\posicionador\\repetibilidad'

# Find the number of the last test run
try: 
    testrun_index = 1 + max(int(filename[3:6]) for filename 
            in listdir(output_directory) if filename[:3]=='run')
except Exception:
    testrun_index = 1

lvdt = LVDT(calibration_file, oscilloscope_resource)

positioner = ESP300('GPIB0::3::INSTR')
positioner.initialize()
# From CMA-12PP manual
positioner.maximum_velocity[axis] = Q_(400,'um/s')
positioner.target_velocity[axis] = positioner.maximum_velocity[axis] * 0.9

# Set current position to 0
# Important: jog the positioner to its center of travel, and adjust the LVDT so
# it reads 0V, _before_ running the program
lvdt.set(Q_(0,'mm'))
positioner.position[axis] = Q_(0,'mm')

# Measure repeatability in 10 uniformly spaced points
lvdt_range = Q_(.1, 'inch').to('mm')
positions = np.linspace(-lvdt_range, lvdt_range, 10)
# Go to each point and then back many times, then measure the dispersion in the
# position measured at each point
cycles = 10
targets = cycles * (list(range(len(positions)))+
                    list(range(len(positions)-2,0,-1))) + [0]

lvdt_reading = Q_(np.zeros((len(targets))),'mm')
positioner_reading = Q_(np.zeros((len(targets))),'mm')

for i,target in enumerate(targets):
    position = positions[target]
    print('{:d}/{:d}: Moving to {:!s}'.format(i+1, len(targets),
                                              position.to('mm')))
    positioner.target_position[axis] = position
    positioner.wait_motion_done()
    # Wait for position to stabilize
    sleep(.1)
    lvdt_reading[i] = lvdt.read()
    positioner_reading[i] = position

print('Returning home')
positioner.target_position[axis] = Q_(0,'mm')

output = open(output_directory + '\\run{:03d}.csv'.format(testrun_index),
              'wb')
headers['axis'] = axis
headers['model'] = positioner.ID[axis]
headers['target_velocity'] = positioner.target_velocity[axis]
headers['cycles'] = cycles
output.write(bytes(''.join('# {:s}={:!s}\n'.format(key, val) for key,val 
                           in headers.iteritems()), 'utf-8'))
# Data format: 2-column CSV file
# First column: positioner readings in mm
# First column: LVDT readings in mm
data = np.vstack([positioner_reading.magnitude, lvdt_reading.magnitude]
                 ).transpose()
np.savetxt(output, data, delimiter=',')
output.close()

# Wait for motion to finish?
#positioner.wait_motion_done()
positioner.finalize()

