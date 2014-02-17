from esp300 import ESP300
import numpy as np
from lantz import Q_
from lvdt import LVDT
from os import listdir
from time import sleep

axis = 1
calibration_file = 'C:\\ignacio\\mediciones\\lvdt\\calibracion lvdt.csv'
oscilloscope_resource = 'GPIB0::14::INSTR'
output_directory = 'C:\\ignacio\\mediciones\\lvdt'
# Number of LVDT readings to take the std of
readings = 100

# Find the number of the last test run
try:
    testrun_index = 1 + max(int(filename[7:10]) for filename 
            in listdir(output_directory) if filename[:7]=='testrun')
except Exception:
    testrun_index = 1

output = open(output_directory + '\\testrun{:03d}.csv'.format(testrun_index),
              'wb')
output.write(bytes('# axis={:d}\n'.format(axis),'utf-8'))

lvdt = LVDT(calibration_file, oscilloscope_resource)

positioner = ESP300('GPIB0::3::INSTR')
positioner.initialize()
# From CMA-12PP manual
positioner.maximum_velocity[axis] = Q_(400,'um/s')
positioner.target_velocity[axis] = positioner.maximum_velocity[axis] * 0.9

output.write(bytes('# model={:s}\n'.format(positioner.ID[axis]),'utf-8'))
output.write(bytes('# readings={:d}\n'.format(readings),'utf-8'))

# Set current position to 0
# Important: jog the positioner to its center of travel, and adjust the LVDT so
# it reads 0V, _before_ running the program
lvdt.set(Q_(0,'mm'))
positioner.position[axis] = Q_(0,'mm')

# LVDT is suposed to go from -10V to 10V,
lvdt_range = Q_(.1, 'inch').to('mm')
targets = np.linspace(-lvdt_range, lvdt_range, 10)
lvdt_std = Q_(np.empty((len(targets))),'mm')
for i,target in enumerate(targets):
    print('Target {:d}: {:!s}'.format(i, target.to('mm')))
    positioner.target_position[axis] = target
    positioner.wait_motion_done()
    # Wait for position to stabilize
    sleep(0.1)
    lvdt_std[i] = np.std(np.array([lvdt.read().to('mm').magnitude 
        for _ in range(readings)])) * Q_(1,'mm')
    print('LVDT standard deviation: {:!s}'.format(lvdt_std[i].to('mm')))

print('Returning home')
positioner.target_position[axis] = Q_(0,'mm')

# Data format: 2-column CSV file
# First column: positioner readings in mm
# First column: LVDT std in mm
data = np.vstack([targets, lvdt_std]).transpose()
np.savetxt(output, data, delimiter=',')
output.close()

# Wait for motion to finish?
#positioner.wait_motion_done()
positioner.finalize()

