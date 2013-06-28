from esp300 import ESP300
import numpy as np
from lantz import Q_
from lvdt import LVDT
from os import listdir
from time import sleep

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

output = open(output_directory + '\\run{:03d}.csv'.format(testrun_index),
              'wb')
output.write(bytes('# axis={:d}\n'.format(axis),'utf-8'))

lvdt = LVDT(calibration_file, oscilloscope_resource)

positioner = ESP300('GPIB0::3::INSTR')
positioner.initialize()
# From CMA-12PP manual
positioner.maximum_velocity[axis] = Q_(400,'um/s')
positioner.target_velocity[axis] = positioner.maximum_velocity[axis] * 0.9

output.write(bytes('# model={:s}\n'.format(positioner.ID[axis]),'utf-8'))
output.write(bytes('# target_velocity={:!s}\n'.format(
             positioner.target_velocity[axis]),'utf-8'))

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
output.write(bytes('# cycles={:d}\n'.format(cycles),'utf-8'))
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

