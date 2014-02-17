import datetime
import numpy as np
import os
import re
import time

from lantz import Q_
from esp300 import ESP300
from HP54616B import HP54616B

""" Measure autocorrelation with slow-scan autocorrelator without stepping
"""

# Configuration
axis = 3
lvdt_channel = 1
# LVDT voltage to start acquiring
lvdt_start_value = Q_(-70, 'mV')
pmt_channel = 2
oscilloscope_resource = 'GPIB0::14::INSTR'
positioner_resource = 'GPIB0::3::INSTR'
output_directory = 'C:\\ignacio\\mediciones\\slowscancontinuo'
output_prefix = 'scan'
output_suffix = '.txt'
progress_indications = 10
measurement_delay = Q_(100,'ms') # Time to wait after reaching a position, for
                                 # everything to stabilize
measurement_delay.ito('s')
# !!! Before running this script, set the home position to where the two path
# lengths coincide !!!
sweep_start = Q_(-200,'um')
sweep_end = Q_(200,'um')

# Find the number of the last run
try:
    file_regex = output_prefix+r'(\d\d\d\d)'+output_suffix
    matches = (re.match(file_regex, filename) 
               for filename in os.listdir(output_directory))
    run_index = 1 + max(int(match.group(1))
                        for match in matches if match is not None)
except ValueError:
    run_index = 1

filename = os.path.join(output_directory, (output_prefix+'{:04d}'
                                           +output_suffix).format(run_index))

# Initialize instruments
positioner = ESP300(positioner_resource)
positioner.initialize()
oscilloscope = HP54616B(oscilloscope_resource)
oscilloscope.initialize()

# Set home to current position
positioner.position[axis] = 0
# From CMA-12PP manual
positioner.maximum_velocity[axis] = Q_(400,'um/s')
positioner.target_velocity[axis] = positioner.maximum_velocity[axis]/2
sweep_time = (sweep_end-sweep_start)/positioner.target_velocity[axis]
# Fit autocorrelation to screen
oscilloscope.timebase_range = sweep_time

#oscilloscope.trigger_source = 'channel{}'.format(lvdt_channel)
#oscilloscope.trigger_level = lvdt_start_value
#oscilloscope.trigger_mode = 'single'
# Osc manual says set complete to 0 for single trigger mode
#oscilloscope.complete_percent = 0

print('Saving to ' + filename)
output = open(filename, 'w')
headers = dict(velocity=positioner.target_velocity[axis],
               axis=positioner.ID[axis] + ' on ' + str(axis))
output.write(''.join('# {} = {}\n'.format(key, val) 
                     for key,val in headers.items()))
output.write('#Position [um],PMT [V], LVDT [V]\n')

print('Moving to initial position')
positioner.target_position[axis] = sweep_start
positioner.wait_motion_done()
print('Sweeping')
#oscilloscope.run()
while True:
    try:
        positioner.target_position[axis] = sweep_end
        positioner.wait_motion_done()
        positioner.target_position[axis] = sweep_start
        positioner.wait_motion_done()
    except Exception as e:
        print('Exiting')
positioner.target_position[axis] = 0
exit()
t, lvdt, signal = oscilloscope.data([1,2])
t.ito('s')
lvdt.ito('V')
signal.ito('V')
# Por las dudas
np.savetxt('raw.txt', (lvdt.magnitude, signal.magnitude))
for ii in range(len(lvdt)):
    output.write('{:e}\t{:e}\n'.format(lvdt[ii].magnitude, signal[ii].magnitude))
#np.savetxt(output, (lvdt.magnitude, signal.magnitude))

