from esp300 import ESP300
import numpy as np
from lantz import Q_
from lvdt import LVDT
from os import listdir
from time import sleep

"""Compare positioner readout with LVDT measurement along positioner range of motion. Analyze output with analyze_data.py
"""
axis = 1
calibration_file = 'C:\\ignacio\\mediciones\\lvdt\\calibracion lvdt.csv'
oscilloscope_resource = 'GPIB0::14::INSTR'
output_directory = 'C:\\ignacio\\mediciones\\posicionador'

# Find the number of the last test run
testrun_index = 1 + max(int(filename[7:10]) for filename 
        in listdir(output_directory) if filename[:7]=='testrun')

lvdt = LVDT(calibration_file, oscilloscope_resource)

positioner = ESP300('GPIB0::3::INSTR')
positioner.initialize()
# From CMA-12PP manual
positioner.maximum_velocity[axis] = Q_(400,'um/s')
positioner.target_velocity[axis] = positioner.maximum_velocity[axis] / 10


# Set current position to 0
# Important: jog the positioner to its center of travel, and adjust the LVDT so
# it reads 0V, _before_ running the program
lvdt.set(Q_(0,'mm'))
positioner.position[axis] = Q_(0,'mm')

# LVDT is suposed to go from -10V to 10V,
lvdt_range = Q_(.1, 'inch').to('mm')
targets = np.linspace(-lvdt_range, lvdt_range, 100)
lvdt_readings = Q_(np.empty((len(targets))),'mm')
positioner_readings = Q_(np.empty((len(targets))),'mm')
for i,target in enumerate(targets):
    print('Target {:d}: {:!s}'.format(i, target.to('mm')))
    positioner.target_position[axis] = target
    positioner.wait_motion_done()
    # Wait for position to stabilize
    sleep(0.1)
    print('LVDT says {:!s}'.format(lvdt.read()))
    lvdt_readings[i] = lvdt.read()
    positioner_readings[i] = positioner.position[axis]

print('Returning home')
positioner.target_position[axis] = Q_(0,'mm')

print(positioner_readings)
print(lvdt_readings)

# Data format: 2-column CSV file
# First column: positioner readings in mm
# First column: LVDT readings in mm
data = np.vstack([positioner_readings, lvdt_readings]).transpose()
headers['axis'] = axis
headers['model'] = positioner.ID[axis]
headers['target_velocity'] = positioner.target_velocity[axis]
output = open(output_directory + '\\testrun{:03d}.csv'.format(testrun_index),
              'wb')
output.write(bytes(''.join('# {:s}={:!s}\n'.format(key, val) for key,val 
                           in headers.iteritems()), 'utf-8'))
np.savetxt(output, data, delimiter=',')
output.close()

# Wait for motion to finish?
#positioner.wait_motion_done()
positioner.finalize()
